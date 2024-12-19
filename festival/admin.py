from django.contrib import admin
from .models import festivalActivities
class festivalActivityAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'is_published', 'published_date')
  list_display_links = ('id', 'title') 
  list_editable = ('is_published',)
  search_fields = ('title', 'summary')
  list_per_page = 25
admin.site.register(festivalActivities, festivalActivityAdmin)

 
 