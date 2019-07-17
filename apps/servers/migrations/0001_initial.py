# Generated by Django 2.2.3 on 2019-07-17 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(help_text='主机名', max_length=48, verbose_name='主机名')),
                ('ip', models.GenericIPAddressField(help_text='IP地址', unique=True, verbose_name='IP地址')),
                ('deploy_user', models.CharField(help_text='远程部署账号', max_length=24, verbose_name='远程部署账号')),
                ('deploy_pwd', models.CharField(help_text='远程部署密码', max_length=128, verbose_name='远程部署密码')),
            ],
            options={
                'db_table': 'server',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='WebServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(help_text='环境', verbose_name='环境')),
                ('server', models.ForeignKey(help_text='关联服务器', on_delete=django.db.models.deletion.PROTECT, to='servers.Server', verbose_name='关联服务器')),
                ('site', models.ForeignKey(help_text='所属站点', on_delete=django.db.models.deletion.PROTECT, to='sites.Site', verbose_name='所属站点')),
            ],
            options={
                'db_table': 'webserver',
                'ordering': ['id'],
                'unique_together': {('site', 'server', 'type')},
            },
        ),
    ]