from rest_framework.routers import DefaultRouter

from opers.views import OperViewSet

oper_router = DefaultRouter()

oper_router.register('oper', OperViewSet, base_name='oper')