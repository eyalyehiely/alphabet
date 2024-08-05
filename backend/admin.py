from django.contrib import admin
from .models import User, Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'starting_time', 'end_time', 'location', 'created_at', 'updated_at')
    search_fields = ('name', 'location')
    filter_horizontal = ('participants',)

admin.site.register(Event, EventAdmin)
