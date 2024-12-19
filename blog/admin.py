from django.contrib import admin
from .models import BlogActivities
class BlogActivityAdmin(admin.ModelAdmin):
 {}
admin.site.register(BlogActivities, BlogActivityAdmin)

 
 