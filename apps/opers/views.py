import threading

from django.shortcuts import render
from rest_framework import viewsets, response, mixins, status

from opers.models import Oper
from opers.serializers import OperSerializer
from opers.filters import OperFilter
from deploy.action import Action
# Create your views here.


class OperViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet,):
    '''
    list:
        返回操作记录
    create:
        新建发布/回滚操作
    update:
        发布线上
    partial_update:
        取消发布
    destroy:
        回滚
    '''
    queryset = Oper.objects.all()
    serializer_class = OperSerializer
    filterset_class = OperFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        site = serializer.validated_data.get("site")
        oper_version = serializer.validated_data.get("oper_version")

        if site.deploy_status:
            return response.Response(status=409)

        if oper_version == site.online_version:
            return response.Response(status=400)

        #
        oper = serializer.save()

        site.deploy_status = True
        site.save()

        oper.deploy_status = 1
        oper.save()

        #
        threading.Thread(target=Action().publish, args=(oper, site)).start()

        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        oper = self.get_object()
        if not oper.oper_status == 1:
            return response.Response(status=400)

        if oper.deploy_status:
            return response.Response(status=409)

        oper.deploy_status = 1
        oper.save()

        #
        threading.Thread(target=Action().publish, args=(oper, oper.site, 1)).start()

        return response.Response(status=status.HTTP_202_ACCEPTED)

    def partial_update(self, request, *args, **kwargs):
        oper = self.get_object()
        if not oper.oper_status == 1:
            return response.Response(status=400)

        if oper.deploy_status:
            return response.Response(status=409)

        oper.deploy_status = 2
        oper.save()

        #
        threading.Thread(target=Action().rollback, args=(oper, oper.site)).start()

        return response.Response(status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        oper = self.get_object()
        if not oper.oper_status == 2:
            return response.Response(status=400)

        site = oper.site
        if site.deploy_status:
            return response.Response(status=409)

        if oper.deploy_status:
            return response.Response(status=409)

        oper.deploy_status = 2
        oper.save()

        site.deploy_status = True
        site.save()

        #
        threading.Thread(target=Action().rollback, args=(oper, site, True)).start()

        return response.Response(status=status.HTTP_202_ACCEPTED)
