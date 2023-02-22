from django.contrib import admin

from apps.calendar.models import Calendar


class CalendarAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'slug', 'color', 'order')
    list_filter = ('user',)


admin.site.register(Calendar, CalendarAdmin)
