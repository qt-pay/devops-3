from django.shortcuts import render
from rest_framework import viewsets, response, mixins

from releases.models import Release
from releases.serializers import ReleaseSerializer
from releases.filters import ReleaseFilter
# Create your views here.


class ReleaseViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    list:
        返回版本列表
    '''
    queryset = Release.objects.all()
    serializer_class = ReleaseSerializer
    filterset_class = ReleaseFilter

