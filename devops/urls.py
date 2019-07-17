"""devops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

route = DefaultRouter()

from servers.router import server_router
from sites.router import site_router
from releases.router import release_router
from opers.router import oper_router
from deploy.router import hook_router

route.registry.extend(server_router.registry)
route.registry.extend(site_router.registry)
route.registry.extend(release_router.registry)
route.registry.extend(oper_router.registry)
route.registry.extend(hook_router.registry)

urlpatterns = [
    path('', include(route.urls)),
    path('docs/', include_docs_urls("运维平台API文档")),
]