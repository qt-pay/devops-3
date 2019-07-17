import django_filters
from releases.models import Release


class ReleaseFilter(django_filters.FilterSet):
    class Meta:
        model = Release
        fields = ['site']
