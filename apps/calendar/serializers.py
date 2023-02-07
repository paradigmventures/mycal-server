from rest_framework import serializers

from apps.calendar.models import Calendar


class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = ['slug', 'title', 'color', 'order']
        lookup_field = 'slug'
