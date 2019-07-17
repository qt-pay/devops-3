from pathlib import Path
from rest_framework.reverse import reverse

#
from sites.models import Site
from releases.models import Release
from opers.models import Oper
from deploy import gl
from deploy.fabric_api import FabricApi
from config import SERVER_NAME, SERVER_PORT, SERVER_IP, CODE_DIR


class Action:

    def init_project(self, site: Site, project):
        commits = gl.get_commits(project)
        for commit in commits:
            Release(site=site, version=commit.id, message=commit.message, committed_time=commit.committed_date).save()
        gl.add_hook(project, "http://{}:{}{}".format(SERVER_NAME if SERVER_NAME else SERVER_IP, SERVER_PORT, reverse('hook-list')))
        site.status = 1
        site.save()

    def flush_commits(self, site: Site, commits):
        for commit in commits:
            Release(site=site, version=commit["id"], message=commit["message"], committed_time=commit["timestamp"]).save()

    def publish(self, oper: Oper, site: Site, server_type=0):
        try:
            # 判断本地代码文件是否存在(不存在则拉取文件)
            path = '{}/{}/{}.tar.gz'.format(CODE_DIR, site.project, oper.oper_version.version)
            p = Path(path)
            if not p.is_file():
                if not p.parent.is_dir():
                    p.parent.mkdir(parents=True, exist_ok=True)

                with open(path, 'wb') as f:
                    f.write(gl.pull_archive(gl.get_project(site.project), oper.oper_version.version))

            # 远程服务器代码保存路径
            dest = "{0}/{1}/{1}-{2}-{3}".format(site.dev_path, site.project, oper.oper_version.version[:8], oper.oper_version.version)

            fbs = set()

            # 过滤指定环境的服务器
            webservers = site.webserver_set.filter(type=server_type).all()
            for webserver in webservers:
                server = webserver.server
                fb = FabricApi(server.ip, server.deploy_user, server.deploy_pwd)
                # 判断代码文件是否存在(不存在则发送文件)
                fb.send_file(path, dest)
                fbs.add(fb)

            #
            for fb in fbs:
                fb.update_symbolic_link(site.site_path, dest)

            oper.oper_status += 1

            if oper.oper_status == 1:
                site.pre_version = oper.oper_version
            else:
                site.pre_version = None
                site.online_version = oper.oper_version
                site.status = 2
                site.deploy_status = False

            oper.deploy_status = 0
            oper.save()
            site.save()
        except:
            self.rollback(oper, site, False if server_type else True)

    def rollback(self, oper: Oper, site: Site, all=False):
        try:
            dest = "{0}/{1}/{1}-{2}-{3}".format(site.dev_path, site.project, oper.online_version.version[:8], oper.online_version.version)

            webservers = site.webserver_set
            if not all:
                webservers = webservers.filter(type=0)

            for webserver in webservers.all():
                server = webserver.server
                FabricApi(server.ip, server.deploy_user, server.deploy_pwd).update_symbolic_link(site.site_path, dest)

            oper.oper_status = 5 if all else 4
            site.online_version = oper.online_version
        except:
            oper.oper_status = 6
            site.status = 3
        finally:
            oper.deploy_status = 0
            oper.save()

            site.deploy_status = False
            site.pre_version = None
            site.save()

    def webserver_offline(self, site: Site):
        # 暂时实现站点信息更新，后期实现站点下线
        if not site.webserver_set.filter(type=0).count() > 0:
            site.pre_version = None
        if not site.webserver_set.filter(type=1).count() > 0:
            site.online_version = None
        if not site.pre_version and not site.online_version:
            site.status = 1
        site.save()
