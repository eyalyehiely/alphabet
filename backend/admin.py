from django.contrib import admin
from .models import *

class EventAdmin(admin.ModelAdmin):
    list_display = ('id','name','starting_time','end_time','location', 'created_at', 'updated_at')
admin.site.register(Event, EventAdmin)


class userAdmin(admin.ModelAdmin):
    list_display = ('id','email','password','end_time','events', 'created_at', 'updated_at')
admin.site.register(User, userAdmin)

class UserEventAdmin(admin.ModelAdmin):
    list_display = ('user','event', 'created_at', 'updated_at')
admin.site.register(UserEvent, UserEventAdmin)