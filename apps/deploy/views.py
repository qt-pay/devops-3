from django.shortcuts import render
from rest_framework import viewsets, response

from sites.models import Site
from deploy.action import Action
# Create your views here.


class HooksViewSet(viewsets.ViewSet):
    '''
    create:
        gitlab钩子函数
    '''

    def create(self, request, *args, **kwargs):
        project_name = request.data.get("project", {}).get("name")
        if not project_name:
            return response.Response(status=400)

        site = Site.objects.filter(project=project_name).first()
        if not site:
            return response.Response(status=404)

        commits = request.data.get("commits", [])
        if not commits or not isinstance(commits, list):
            return response.Response(status=400)

        try:
            Action().flush_commits(site, commits)
        except Exception as e:
            return response.Response(status=400)

        return response.Response()
