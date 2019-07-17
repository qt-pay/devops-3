import gitlab


class GitlabApi:
    def __init__(self, url, token):
        self.gl = gitlab.Gitlab(url, token)

    def get_project(self, project_name):
        projects = self.gl.projects.list(search=project_name)
        for project in projects:
            if project.name == project_name:
                return project

    def get_commits(self, project):
        return project.commits.list(all=True)

    def pull_archive(self, project: gitlab, commit_id):
        return project.repository_archive(sha=commit_id[:8])

    def add_hook(self, project, url, push_events=True, branch="master", ssl=False):
        return project.hooks.create({
            'url': url,
            'push_events': push_events,
            'push_events_branch_filter': branch,
            'enable_ssl_verification': ssl
        })
