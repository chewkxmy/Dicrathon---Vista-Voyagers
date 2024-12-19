from django.db import models
from django.contrib.auth.models import User 
from datetime import datetime
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
from category.models import CategoryActivities

class BlogActivities(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    user_selection = models.ManyToManyField(CategoryActivities)
    created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    def get_selection_details(self):
        selections = []
        for selection in self.user_selection.all():
            details = {
                "title": selection.title,
                "id": selection.id,
                "content": selection.content,
                "photo_main": selection.photo_main,
                "latitude": selection.latitude,
                "longitude": selection.longitude,
                "maplink": selection.maplink,
                "address": selection.address,
                "monday": selection.monday,
                "tuesday": selection.tuesday,
                "wednesday": selection.wednesday,
                "thursday": selection.thursday,
                "friday": selection.friday,
                "saturday": selection.saturday,
                "sunday": selection.sunday,
                "contact": selection.contact,
                "fee": selection.fee,
                "rating": selection.rating,
                "website_link": selection.website_link,
            }
            selections.append(details)
        return selections
    
    class Beta:
        unique_together = ('user', 'user_selection')  # Prevent duplicate selections for the same user and activity
   
    




