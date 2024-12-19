from django.contrib import admin
from .models import CategoryActivities
class CategoryActivityAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'is_published', 'published_date')
  list_display_links = ('id', 'title') 
  list_editable = ('is_published',)
  search_fields = ('title', 'summary')
  list_per_page = 30
admin.site.register(CategoryActivities, CategoryActivityAdmin)

 
 