from config import GITLAB_URL, GITLAB_TOKEN
from deploy.gitlab_api import GitlabApi


gl = GitlabApi(GITLAB_URL, GITLAB_TOKEN)
