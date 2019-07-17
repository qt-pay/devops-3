from rest_framework.routers import DefaultRouter

from sites.views import SiteViewSet, SiteListViewSet

site_router = DefaultRouter()

site_router.register('site', SiteViewSet, base_name='site')
site_router.register('sitelist', SiteListViewSet, base_name='sitelist')
