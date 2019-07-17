from django.db import models
# from sites.models import Site

# Create your models here.


class Release(models.Model):
    site = models.ForeignKey("sites.Site", verbose_name="所属站点", help_text="所属站点", on_delete=models.PROTECT)
    version = models.CharField(max_length=48, verbose_name="版本ID", help_text="版本ID")
    message = models.CharField(max_length=256, verbose_name="更改描述", help_text="更改描述")
    committed_time = models.DateTimeField(verbose_name="提交时间", help_text="提交时间")

    class Meta:
        db_table = "release"
        unique_together = (("site", "version"),)
        ordering = ["-committed_time"]

    def __str__(self):
        return "<Release: ({} {} {})>".format(self.site.project, self.version[:8], self.message)
