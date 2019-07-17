from django.db import models
# from sites.models import Site
# from releases.models import Release
# Create your models here.


class Oper(models.Model):
    site = models.ForeignKey("sites.Site", verbose_name="所属站点", help_text="所属站点", on_delete=models.PROTECT)
    oper_time = models.DateTimeField(verbose_name="操作时间", help_text="操作时间", auto_now_add=True)
    oper_version = models.ForeignKey("releases.Release", related_name="oper", verbose_name="操作版本", help_text="操作版本", on_delete=models.PROTECT)
    online_version = models.ForeignKey("releases.Release", related_name="online_oper", null=True, verbose_name="线上版本", help_text="线上版本", on_delete=models.PROTECT)
    deploy_status = models.IntegerField(default=0, verbose_name="部署状态", help_text="部署状态")    # 0-空闲,1-正在发布,2-正在回滚
    oper_status = models.IntegerField(default=0, verbose_name="操作状态", help_text="操作状态")
    # 0-正在预发布,1-预发布成功,2-发布成功,3-发布失败,4-取消发布,5-已回滚,6-回滚失败

    class Meta:
        db_table = "oper"
        ordering = ["-oper_time"]

    def __str__(self):
        return "<Oper: ({} {})>".format(self.site.name, self.oper_status)
