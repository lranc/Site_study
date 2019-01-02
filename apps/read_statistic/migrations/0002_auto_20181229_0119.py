# Generated by Django 2.0 on 2018-12-28 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_statistic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='readdetail',
            name='read_object',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='阅读对象名'),
        ),
        migrations.AlterField(
            model_name='readdetail',
            name='read_num',
            field=models.IntegerField(default=0, verbose_name='当天阅读次数'),
        ),
        migrations.AlterField(
            model_name='readnum',
            name='read_num',
            field=models.IntegerField(default=0, verbose_name='阅读次数'),
        ),
    ]