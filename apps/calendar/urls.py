from django.urls import path

from apps.calendar.views import CalendarList, CalendarDetail


app_name = 'calendar'

urlpatterns = [
    path('calendars', CalendarList.as_view(), name='list'),
    path('calendar/<slug:slug>', CalendarDetail.as_view(), name='detail'),
]
