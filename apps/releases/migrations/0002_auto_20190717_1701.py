# Generated by Django 2.2.3 on 2019-07-17 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('releases', '0001_initial'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='site',
            field=models.ForeignKey(help_text='所属站点', on_delete=django.db.models.deletion.PROTECT, to='sites.Site', verbose_name='所属站点'),
        ),
        migrations.AlterUniqueTogether(
            name='release',
            unique_together={('site', 'version')},
        ),
    ]
