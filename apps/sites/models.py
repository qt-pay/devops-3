from django.db import models
# from releases.models import Release

# Create your models here.


class Site(models.Model):
    name = models.CharField(max_length=128, verbose_name="站点名称/地址", help_text="站点名称/地址", unique=True)
    project = models.CharField(max_length=128, verbose_name="gitlab项目名称", help_text="gitlab项目名称", unique=True)
    dev_path = models.CharField(max_length=128, verbose_name="代码保存路径", help_text="代码保存路径")
    site_path = models.CharField(max_length=128, verbose_name="站点目录", help_text="站点目录")
    online_version = models.ForeignKey("releases.Release", related_name="online_site", null=True, verbose_name="线上版本", help_text="线上版本", on_delete=models.PROTECT)
    pre_version = models.ForeignKey("releases.Release", related_name="pre_site",null=True, verbose_name="预发布版本", help_text="预发布版本", on_delete=models.PROTECT)
    deploy_status = models.BooleanField(default=False, verbose_name="发布状态", help_text="发布状态")   # False,-空闲,True-正在发布
    status = models.IntegerField(default=0, verbose_name="状态", help_text="状态")
    # 0-初始化,1-未发布,2-正常,3-异常

    class Meta:
        db_table = "site"
        ordering = ["id"]

    def __str__(self):
        return "<Site: ({})>".format(self.name)
