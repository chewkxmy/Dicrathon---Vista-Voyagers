from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .forms import FlightDetailsForm  
from blog.models import BlogActivities
from category.models import CategoryActivities
from festival.models import festivalActivities
from datetime import datetime, timedelta
import requests

def index_view(request):
    category = CategoryActivities.objects.filter(category='Culinary Excellence').order_by('?')[:6]
    blog = BlogActivities.objects.all()
    festival = festivalActivities.objects.all()
    form = FlightDetailsForm()
    content = {
        'blog': blog,
        'form': form,
        'category': category,
        'festival': festival,
         
    }
    return render(request, 'pages/index.html', content)

def test(request):
    return render(request, 'pages/test.html')

def keywords_view(request):
    form = FlightDetailsForm()

    if request.method == 'POST':
        # Get the selected keywords from the form submission
        selected_keywords = request.POST.get('keywords', '')
        
        # Get start and end dates from the form submission
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Store them in the session
        request.session['selected_keywords'] = selected_keywords.split(',')
        request.session['start_date'] = start_date
        request.session['end_date'] = end_date

        # Redirect to the planner page
        return redirect('planner')

    return render(request, 'pages/keywords.html', {'form': form})

def favourite_view(request):
    # Assuming you have a way to get the user's favorite places
    favourite = []  # Replace this with your method to get favorite places

    # Example: Get all favorite places from the session (if you are storing them there)
    if 'favourites' in request.session:
        favourite = CategoryActivities.objects.filter(id__in=request.session['favourite'])

    return render(request, 'pages/favourite.html', {'favourite': favourite})


def festival_details_view(request, id):
    festival = festivalActivities.objects.filter(id=id)   
    return render(request, 'pages/festival_details.html', {'festival': festival})  # Pass the single festival object

def place_details_view(request, id):
    try:
        place = CategoryActivities.objects.get(id=id)  # Fetch a single place by ID
    except CategoryActivities.DoesNotExist:
        # Redirect or render a 404 page if place is not found
        return render(request, 'pages/404.html')
    
# Pass the selected category back to the place details template
    selected_category = place.category  # Assuming category is a field in your model

# Define categories for fee and price range
    fee_categories = [
        "Cultural Heritage",
        "Nature and Scenery",
        "Arts and Culture",
        "Unique Landmarks and Experience",
        "Adventures",
        "Museums"
    ]
    price_range_categories = [
        "Culinary Excellence",
        "Restaurants and Cafes"
    ]

    return render(request, 'pages/place_details.html', {
        'place': place,
        'selected_category': selected_category,
        'fee_categories': fee_categories,
        'price_range_categories': price_range_categories,
    })  # Pass the single place

def nature_view(request):
    category = CategoryActivities.objects.filter(category='Nature and Scenery')
    content = {
        'category': category,
    }
    return render(request, 'pages/nature.html', content)

def place_category_view(request):
    # Get the selected category from the request
    selected_category = request.GET.get('category', 'Nature and Scenery')  # Default category

    # Fetch places based on the selected category
    places = CategoryActivities.objects.filter(category=selected_category)

    content = {
        'category': places,
        'selected_category': selected_category,
    }
    return render(request, 'pages/place_category.html', content)

def planner_view(request):
    # Retrieve dates, keywords, and selected places from session
    start_date = request.session.get('start_date', 'Not selected')
    end_date = request.session.get('end_date', 'Not selected')
    selected_keywords = request.session.get('selected_keywords', [])
    
    # Format dates to match the expected format in the placeholders
    if start_date and start_date != 'Not selected':
        start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%d-%m-%Y')
    if end_date and end_date != 'Not selected':
        end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d-%m-%Y')

    # Fetch activities based on selected keywords
    activities = CategoryActivities.objects.filter(category__in=selected_keywords)

    # Fetch weather data
    latitude = 5.5282142  # Replace with actual latitude
    longitude = 100.3805536  # Replace with actual longitude
    weather_forecast = fetch_weather_forecast(latitude, longitude)
    
    if weather_forecast:
        for day in weather_forecast:
            # Format weather descriptions and icons
            day['formatted_weather'] = get_formatted_description(day['weather'])
            day['weather_icon'] = get_weather_icon(day['weather'])
            day['hourly_data'] = [
                {
                    'datetime': entry['datetime'],
                    'time': entry['datetime'].strftime('%H:%M'),
                    'temp2m': entry['temp2m'],
                    'weather': get_formatted_description(entry['weather']),
                    'weather_icon': get_weather_icon(entry['weather'])
                }
                for entry in day['hourly_data']
            ]

    if request.method == 'POST':
        # Handle form submission for selected places
        selected_places = request.POST.getlist('places[]')
        request.session['selected_places'] = selected_places
        return redirect('planner2')  # Redirect to the next page (if needed)

    # Prepare context for the template
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'selected_keywords': selected_keywords,
        'activities': activities,
        'weather_forecast': weather_forecast,
        'latitude': latitude,
        'longitude': longitude
    }

    return render(request, 'pages/planner.html', context)

def fetch_weather_forecast(latitude, longitude):
    base_url = "http://www.7timer.info/bin/api.pl"
    params = {
        "lon": longitude,
        "lat": latitude,
        "product": "civil",
        "output": "json"
    }

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        print("Error fetching data:", response.status_code)
        return None

    weather_data = response.json().get("dataseries", [])
    forecast_14_days = []
    forecast_start = datetime.utcnow()
    current_date = None
    daily_summary = {}
    day_count = 0

    for entry in weather_data:
        entry_datetime = forecast_start + timedelta(hours=entry["timepoint"])
        date = entry_datetime.date()

        if current_date != date:
            if current_date and day_count < 14:
                forecast_14_days.append(daily_summary)
                day_count += 1
            
            current_date = date
            daily_summary = {
                "date": current_date,
                "temp2m": [],
                "weather": [],
                "hourly_data": []
            }

        daily_summary["temp2m"].append(entry["temp2m"])
        daily_summary["weather"].append(entry["weather"])

        hourly_entry = {
            "datetime": entry_datetime,
            "temp2m": entry["temp2m"],
            "weather": entry["weather"]
        }
        daily_summary["hourly_data"].append(hourly_entry)

    if day_count < 14:
        forecast_14_days.append(daily_summary)

    for day in forecast_14_days:
        day["avg_temp2m"] = sum(day["temp2m"]) / len(day["temp2m"])
        day.pop("temp2m")
        day["weather"] = max(set(day["weather"]), key=day["weather"].count)
    
    return forecast_14_days


def get_weather_icon(weather_description):
    weather_icons = {
        "clearday": "☀️",
        "clearnight": "☀️",
        "pcloudyday": "⛅",
        "pcloudynight": "⛅",
        "mcloudyday": "☁️",
        "mcloudynight": "☁️",
        "cloudyday": "☁️☁️",
        "cloudynight": "☁️☁️",
        "humidday": "🌫️",
        "humidnight": "🌫️",
        "lightrainday": "🌦️",
        "lightrainnight": "🌦️",
        "rainday": "🌧️",
        "rainnight": "🌧️",
        "ishowerday": "🌦️",
        "ishowernight": "🌦️",
        "oshowerday": "🌧️",
        "oshowernight": "🌧️",
        "lightsnowday": "🌨️",
        "lightsnownight": "🌨️",
        "snowday": "❄️",
        "snownight": "❄️",
        "rainsnowday": "🌧️❄️",
        "rainsnownight": "🌧️❄️",
        "tsday": "🌩️",
        "tsnight": "🌩️",
        "tsrainday": "⛈️",
        "tsrainnight": "⛈️",
    }

    for key, icon in weather_icons.items():
        if key in weather_description.lower():
            return icon
    
    return "🌥️"


def get_formatted_description(weather_description):
    weather_descriptions = {
        "clearday": "Clear Day",
        "clearnight": "Clear Night",
        "pcloudyday": "Partly Cloudy Day",
        "pcloudynight": "Partly Cloudy Night",
        "mcloudyday": "Mostly Cloudy Day",
        "mcloudynight": "Mostly Cloudy Night",
        "cloudyday": "Cloudy Day",
        "cloudynight": "Cloudy Night",
        "humidday": "Humid Day",
        "humidnight": "Humid Night",
        "lightrainday": "Light Rain Day",
        "lightrainnight": "Light Rain Night",
        "rainday": "Rain Day",
        "rainnight": "Rain Night",
        "ishowerday": "Ishower Day",
        "ishowernight": "Ishower Night",
        "oshowerday": "Oshower Day",
        "oshowernight": "Oshower Night",
        "lightsnowday": "Light Snow Day",
        "lightsnownight": "Light Snow Night",
        "snowday": "Snow Day",
        "snownight": "Snow Night",
        "rainsnowday": "Rain Snow Day",
        "rainsnownight": "Rain Snow Night",
        "tsday": "Thunderstorm Day",
        "tsnight": "Thunderstorm Night",
        "tsrainday": "Thunderstorm Rain Day",
        "tsrainnight": "Thunderstorm Rain Night",
    }

    normalized_description = weather_description.lower()
    
    for key in weather_descriptions.keys():
        if key in normalized_description:
            return weather_descriptions[key]

    return "Unknown Weather"

