from django.db import models
from django.contrib.auth.models import User 
from datetime import datetime
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify

class festivalActivities(models.Model):
    id = models.BigAutoField(primary_key=True)
    header = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    content = CKEditor5Field()
    estimated_date = models.CharField(max_length=200)  # New field for operating hours
    in_outDoor = models.CharField(max_length=50)  # Updated field name
    website = models.URLField(max_length=200)
    
    #photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_main = models.URLField(max_length=200)  
    is_published = models.BooleanField(default=True)
    published_date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = f"{base_slug}-{self.id}" if self.id else base_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

