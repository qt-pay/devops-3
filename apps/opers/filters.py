import django_filters
from opers.models import Oper


class OperFilter(django_filters.FilterSet):
    class Meta:
        model = Oper
        fields = ['site']
