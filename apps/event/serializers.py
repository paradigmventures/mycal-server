from rest_framework import serializers

from apps.calendar.models import Calendar
from apps.event.models import Event


class EventSerializer(serializers.ModelSerializer):
    """
    This Serializer is used in two contexts during the same request/response cycle
    1) param_filtering context for validating: calendars (comma-delimited slug list), start_date, end_date
    2) queryset context for serializing: model data into json
    """
    # NOTE: not actually a model field, only for param_filtering context
    calendars = serializers.ListField(child=serializers.SlugField(), required=False)
    # NOTE: required=False is only for 1st-pass param_filtering execution to complete (both fields below)
    calendar = serializers.SlugRelatedField(slug_field='slug', queryset=Calendar.objects.all(), required=False)
    title = serializers.CharField(required=False)

    class Meta:
        model = Event
        # NOTE: including 'calendars' stub field to enable 2nd-pass execution to complete
        fields = ['calendar', 'calendars', 'uuid', 'title', 'is_all_day', 'start_date', 'start_datetime',
                  'end_date', 'end_datetime', 'description']
        lookup_field = 'uuid'
