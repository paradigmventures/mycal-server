from django.urls import path

from apps.event.views import EventList, EventDetail


app_name = 'event'

urlpatterns = [
    path('events', EventList.as_view(), name='list'),
    path('event/<uuid:uuid>', EventDetail.as_view(), name='detail'),
]
