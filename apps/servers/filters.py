import django_filters
from django.db.models import Q

from servers.models import Server, WebServer


class ServerFilter(django_filters.FilterSet):
    hostname = django_filters.CharFilter(method='search_hostname')

    def search_hostname(self, qs, name, value):
        return qs.filter(Q(hostname__icontains=value) | Q(ip__icontains=value))

    class Meta:
        model = Server
        fields = ['hostname']


class WebServerFilter(django_filters.FilterSet):
    class Meta:
        model = WebServer
        fields = ['site']

