from rest_framework import generics

from apps.calendar.models import Calendar
from apps.calendar.serializers import CalendarSerializer


class CalendarList(generics.ListCreateAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer


class CalendarDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
    lookup_field = 'slug'
