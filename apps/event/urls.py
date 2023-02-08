from django.urls import path

from apps.event.views import EventList, EventListByCalendar, EventDetail


app_name = 'event'

urlpatterns = [
    path('events', EventList.as_view(), name='list'),
    path('events/<slug:calendar_slug>', EventListByCalendar.as_view(), name='list-by-calendar'),
    path('event/<uuid:uuid>', EventDetail.as_view(), name='detail'),
]
