from rest_framework import generics
from rest_framework.response import Response

from apps.event.models import Event
from apps.event.serializers import EventSerializer


class EventList(generics.ListCreateAPIView):
    serializer_class = EventSerializer

    def list(self, request, *args, **kwargs):
        response_data = []
        query_params = self.parse_query_params()
        # NOTE: 1st pass validating url query params
        param_serializer = self.get_serializer(data=query_params)
        if param_serializer.is_valid(raise_exception=True):
            queryset = self.filter_queryset(self.get_queryset(), params=param_serializer.validated_data)
            # NOTE: 2nd pass serializing model data into json
            model_serializer = self.get_serializer(queryset, many=True)
            response_data = model_serializer.data
        return Response(response_data)

    def parse_query_params(self):
        query_params = self.request.query_params.dict()
        if query_params.get('calendars', None):
            query_params['calendars'] = query_params['calendars'].split(',')
        return query_params

    def get_queryset(self):
        return Event.objects.filter(calendar__user=self.request.user,
                                    is_all_day=True)  # TODO tmp

    def filter_queryset(self, queryset, params=None):
        # optional: date range
        if params.get('start_date', None):
            queryset = queryset.filter(start_date__gte=params['start_date'])
        if params.get('end_date', None):
            queryset = queryset.filter(start_date__lte=params['end_date'])
        # optional: calendar list
        if params.get('calendars', None):
            queryset = queryset.filter(calendar__slug__in=params['calendars'])
        # TODO add filtering by location, tags (pre-req: model field indexing for lookup)
        return queryset


class EventListByCalendar(generics.ListAPIView):
    # TODO add filtering by query_param
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(calendar__user=self.request.user,
                                    calendar__slug=self.kwargs['calendar_slug'],
                                    is_all_day=True)  # TODO tmp


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Event.objects.filter(calendar__user=self.request.user)
