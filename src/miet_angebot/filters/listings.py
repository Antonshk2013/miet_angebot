from django_filters import rest_framework as filters

from src.commons.choices import CountRumsChoice
from src.miet_angebot.models import Listing

class ListingFilter(filters.FilterSet):
    price_from = filters.NumberFilter(
        field_name='price_per_day',
        lookup_expr='gte'
    )
    price_to = filters.NumberFilter(
        field_name='price_per_day',
        lookup_expr='lte'
    )

    location = filters.CharFilter(
        field_name='location',
        lookup_expr='icontains')

    rooms_min = filters.NumberFilter(method='filter_rooms')
    rooms_max = filters.NumberFilter(method='filter_rooms')
    type = filters.CharFilter(
        field_name='apartment_type',
    lookup_expr='iexact')

    class Meta:
        model = Listing
        fields = [
            'price_from',
            'price_to',
            'location',
            'type'
        ]

    def filter_rooms(self, queryset, name, value):
         min_value = self.data.get('rooms_min')
         max_value = self.data.get('rooms_max')
         data = CountRumsChoice.filter_by_int_map(min_value, max_value)
         return queryset.filter(rooms_count__in=data)
