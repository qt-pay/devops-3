from rest_framework.routers import DefaultRouter

from releases.views import ReleaseViewSet

release_router = DefaultRouter()

release_router.register('release', ReleaseViewSet, base_name='release')
