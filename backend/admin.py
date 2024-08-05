from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'starting_time', 'end_time', 'location', 'created_at', 'updated_at', 'display_participants')
    search_fields = ('name', 'location')
    filter_horizontal = ('participants',)

    def display_participants(self, obj):
        return ", ".join([participant.username for participant in obj.participants.all()])
    display_participants.short_description = 'Participants'

admin.site.register(Event, EventAdmin)