from django.contrib import admin

from apps.event.models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_dt', 'end_dt', 'calendar')
    list_filter = ('calendar',)


admin.site.register(Event, EventAdmin)
