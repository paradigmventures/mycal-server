from rest_framework import generics

from apps.calendar.models import Calendar
from apps.calendar.serializers import CalendarSerializer


class CalendarList(generics.ListCreateAPIView):
    serializer_class = CalendarSerializer

    def get_queryset(self):
        return Calendar.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CalendarDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CalendarSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Calendar.objects.filter(user=self.request.user)
