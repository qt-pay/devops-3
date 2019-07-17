import threading

from django.shortcuts import render
from rest_framework import viewsets, response, mixins, status

from servers.models import Server, WebServer
from servers.serializers import ServerSerializer, WebServerSerializer, ServerSimpleSerializer
from servers.filters import ServerFilter, WebServerFilter
from deploy.action import Action

# Create your views here.


class ServerViewSet(viewsets.ModelViewSet):
    '''
    retrieve:
        返回指定服务器信息
    list:
        返回服务器列表
    update:
        更新服务器信息
    destroy:
        删除服务器
    create:
        创建服务器
    partial_update:
        更新服务器部分信息
    '''
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    filterset_class = ServerFilter


class ServerListViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    '''
    list:
        返回站点列表，不分页
    '''
    queryset = Server.objects.all()
    serializer_class = ServerSimpleSerializer
    filterset_class = ServerFilter
    pagination_class = None


class WebServerViewSet(viewsets.ModelViewSet):
    '''
    retrieve:
        返回指定WEB服务器信息
    list:
        返回WEB服务器列表
    update:
        更新WEB服务器信息
    destroy:
        删除WEB服务器
    create:
        创建WEB服务器
    partial_update:
        更新WEB服务器部分信息
    '''
    queryset = WebServer.objects.all()
    serializer_class = WebServerSerializer
    filterset_class = WebServerFilter

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        site = instance.site
        self.perform_destroy(instance)

        threading.Thread(target=Action().webserver_offline, args=(site,)).start()

        return response.Response(status=status.HTTP_204_NO_CONTENT)

