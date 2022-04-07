import django_filters

from event.models import Event


class EventFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter()
    order_by = django_filters.OrderingFilter(
        fields=(
            ('clicks', 'clicks'),
            ('views', 'views'),
            ('costs', 'costs'),

             )
        )
    class Meta:
        model = Event
        fields = ['date']