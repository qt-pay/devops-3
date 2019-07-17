from django.db import models
# from sites.models import Site
# Create your models here.


class Server(models.Model):
    hostname = models.CharField(max_length=48, verbose_name="主机名", help_text="主机名")
    ip = models.GenericIPAddressField(unique=True, verbose_name="IP地址", help_text="IP地址")
    deploy_user = models.CharField(max_length=24, verbose_name="远程部署账号", help_text="远程部署账号")
    deploy_pwd = models.CharField(max_length=128, verbose_name="远程部署密码", help_text="远程部署密码")

    class Meta:
        db_table = "server"
        ordering = ["id"]

    def __str__(self):
        return "<Server: ({} {})>".format(self.hostname, self.ip)


class WebServer(models.Model):
    site = models.ForeignKey("sites.Site", verbose_name="所属站点", help_text="所属站点", on_delete=models.PROTECT)
    server = models.ForeignKey(Server, verbose_name="关联服务器", help_text="关联服务器", on_delete=models.PROTECT)
    type = models.IntegerField(verbose_name="环境", help_text="环境")  # 0-预发布,1-线上

    class Meta:
        db_table = "webserver"
        unique_together = (("site", "server", "type"),)
        ordering = ["id"]


    def __str__(self):
        return "<WebServer: ({} {} {})>".format(self.site.name, self.server.hostname, self.type)
