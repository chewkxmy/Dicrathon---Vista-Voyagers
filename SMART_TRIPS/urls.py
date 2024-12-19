from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.urls import path
from . import views
from .views import index_view,test, keywords_view, favourite_view, planner_view,festival_details_view, place_category_view, place_details_view

urlpatterns = [
     
    path('', index_view, name='index'), 
    path('test',test, name='test'),
    path('keywords/', keywords_view, name='pages/keywords'),    
    path('favourite/', favourite_view, name='pages/favourite'),
    path('planner/',planner_view, name='planner'),
    path('festival/<int:id>/', festival_details_view, name='festival_details'),  # Adjust the path as necessary  
    path('place_category/', place_category_view, name='place_category'),   
    path('place/<int:id>/', place_details_view, name='place_details'),
    path('place_category/<str:category>/', place_category_view, name='place_category2'),

    path('accounts/', include('accounts.urls')), 
    path('category/', include('category.urls')),  
    path('festival/', include('festival.urls')),  
    path('admin/', admin.site.urls),
    path('ckeditor5/', include('django_ckeditor_5.urls')), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)