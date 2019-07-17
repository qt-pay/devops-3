from django.shortcuts import render
from rest_framework import viewsets, response, mixins, status
import threading

from sites.models import Site
from sites.serializers import SiteSerializer, SiteSimpleSerializer
from deploy import gl
from deploy.action import Action
# Create your views here.


class SiteViewSet(viewsets.ModelViewSet):
    '''
    retrieve:
        返回指定站点信息
    list:
        返回站点列表
    update:
        更新站点信息
    destroy:
        删除站点
    create:
        创建站点
    partial_update:
        更新站点部分信息
    '''
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 判断项目是否存在
        project_name = serializer.validated_data.get("project")
        project = gl.get_project(project_name)
        if not project:
            return response.Response("Project '{}' does not exist.".format(project_name), status=status.HTTP_400_BAD_REQUEST)

        site = serializer.save()

        # 初始化项目
        threading.Thread(target=Action().init_project, args=(site, project)).start()

        #
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SiteListViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    '''
    list:
        返回站点列表，不分页
    '''
    queryset = Site.objects.all()
    serializer_class = SiteSimpleSerializer
    pagination_class = None

