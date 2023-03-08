from django.contrib import admin

from apps.event.models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'calendar')
    list_filter = ('calendar',)


admin.site.register(Event, EventAdmin)
