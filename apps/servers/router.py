from rest_framework.routers import DefaultRouter

from servers.views import ServerViewSet, WebServerViewSet, ServerListViewSet

server_router = DefaultRouter()

server_router.register('server', ServerViewSet, base_name='server')
server_router.register('serverlist', ServerListViewSet, base_name='serverlist')
server_router.register('webserver', WebServerViewSet, base_name='webserver')
