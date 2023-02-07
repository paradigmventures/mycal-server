from rest_framework import serializers

from apps.calendar.models import Calendar
from apps.event.models import Event


class EventSerializer(serializers.ModelSerializer):
    calendar = serializers.SlugRelatedField(slug_field='slug', queryset=Calendar.objects.all())

    class Meta:
        model = Event
        fields = ['calendar', 'uuid', 'title', 'start_dt', 'end_dt', 'description']
        lookup_field = 'uuid'
