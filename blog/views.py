from django.shortcuts import render
from django.http import HttpResponse
# itinerary_app/views.py
from django.shortcuts import render
from category.models import CategoryActivities
from sklearn.cluster import KMeans
from scipy.spatial.distance import pdist, squareform
import numpy as np


def bogList(request):
    return HttpResponse("Hello, world. You're at the bog list.")



def haversine(lat1, lon1, lat2, lon2):
    from math import radians, sin, cos, sqrt, atan2
    R = 6371  # Radius of Earth in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def calculate_optimal_route(day_locations):
    distances = squareform(pdist(day_locations, lambda u, v: haversine(u[0], u[1], v[0], v[1])))
    n = len(day_locations)
    visited = [False] * n
    route = [0]
    visited[0] = True
    for _ in range(1, n):
        last = route[-1]
        next_loc = np.argmin([distances[last][j] if not visited[j] else np.inf for j in range(n)])
        route.append(next_loc)
        visited[next_loc] = True
    return route

def itinerary_view(request):
    activities = CategoryActivities.objects.filter(is_published=True).order_by('?')[:20]
    coordinates = np.array([(act.latitude, act.longitude) for act in activities if act.latitude and act.longitude])

    kmeans = KMeans(n_clusters=3, random_state=0)
    kmeans.fit(coordinates)
    clusters = kmeans.labels_

    day_activities = {i: [] for i in range(3)}
    for idx, activity in enumerate(activities):
        day_activities[clusters[idx]].append(activity)

    ordered_day_activities = {}
    for day, activities in day_activities.items():
        coords = [(act.latitude, act.longitude) for act in activities]
        order = calculate_optimal_route(coords)
        ordered_day_activities[f'Day {day + 1}'] = [activities[i] for i in order]

    # Context with explicit day labels
    context = {
        'day_activities': {
            'Day 1': ordered_day_activities.get('Day 1', []),
            'Day 2': ordered_day_activities.get('Day 2', []),
            'Day 3': ordered_day_activities.get('Day 3', []),
        }
    }
    return render(request, 'planner2.html', context)