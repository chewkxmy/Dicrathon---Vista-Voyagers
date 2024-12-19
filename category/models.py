from django.db import models
from django.contrib.auth.models import User 
from datetime import datetime
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify

CATEGORY_CHOICES = (
    ('heritage', 'Cultural Heritage'),
    ('nature', 'Nature and Scenery'),
    ('culinary', 'Culinary Excellence'),
    ('festival', 'Festivals and Events'),
    ('arts', 'Arts and Culture'),
    ('crafts', 'Local Crafts and Souvenirs'),
    ('landmark', 'Unique Landmark and Experiences'),
    ('adventure', 'Adventures'),
    ('mall', 'Shopping Malls'),
    ('street', 'Streets and Night markets'),
    ('museum', 'Museums'),
    ('restaurant', 'Restaurants and Cafes'),

    )
class CategoryActivities(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = CKEditor5Field()
    content_more = CKEditor5Field()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # New field for latitude
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # New field for longitude
    maplink = models.URLField(max_length=500)
    address = models.CharField(max_length=200)
    monday = models.CharField(max_length=200)  # New field for operating hours
    tuesday = models.CharField(max_length=200)  # New field for operating hours
    wednesday = models.CharField(max_length=200)  # New field for operating hours
    thursday = models.CharField(max_length=200)  # New field for operating hours
    friday = models.CharField(max_length=200)  # New field for operating hours
    saturday = models.CharField(max_length=200)  # New field for operating hours
    sunday = models.CharField(max_length=200)  # New field for operating hours
    contact = models.CharField(max_length=15)  # New field for contact number
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES)
    fee=models.CharField(max_length=200)
    in_outDoor = models.CharField(max_length=50)  # Updated field name
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # New field for numeric rating
    website_link = website_link = models.URLField(blank=True, null=True)  # New field for website link

    #photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_main = models.URLField(max_length=200)  
    is_published = models.BooleanField(default=True)
    published_date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.title

