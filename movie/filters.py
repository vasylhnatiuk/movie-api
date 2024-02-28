# filters.py
import django_filters
from .models import Movie


class MovieFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    year = django_filters.NumberFilter(field_name='year')
    actor = django_filters.NumberFilter(field_name='actors__id')
    director = django_filters.NumberFilter(field_name='director__id')

    class Meta:
        model = Movie
        fields = ['title', 'year', 'actor', 'director']


class PersonFilter(django_filters.FilterSet):
    specialization = django_filters.CharFilter(field_name="specialization")

    class Meta:
        model = Movie
        fields = ['specialization']
