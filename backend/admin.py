from django.contrib import admin
from .models import User, Event

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'password', 'created_at', 'updated_at')
    search_fields = ('email',)

class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'starting_time', 'end_time', 'location', 'created_at', 'updated_at')
    search_fields = ('name', 'location')


admin.site.register(User, UserAdmin)
admin.site.register(Event, EventAdmin)
