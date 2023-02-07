from django.contrib import admin

from apps.calendar.models import Calendar


class CalendarAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'color', 'order')


admin.site.register(Calendar, CalendarAdmin)
