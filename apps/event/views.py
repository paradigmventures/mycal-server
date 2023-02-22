from rest_framework import generics

from apps.event.models import Event
from apps.event.serializers import EventSerializer


class EventList(generics.ListCreateAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(calendar__user=self.request.user)


class EventListByCalendar(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(calendar__user=self.request.user,
                                    calendar__slug=self.kwargs['calendar_slug'])


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Event.objects.filter(calendar__user=self.request.user)
