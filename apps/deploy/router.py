from rest_framework.routers import DefaultRouter

from deploy.views import HooksViewSet

hook_router = DefaultRouter()

hook_router.register('hook', HooksViewSet, base_name='hook')
