# Generated by Django 2.0 on 2019-01-02 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0003_auto_20190102_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='novel',
            name='click_num',
            field=models.IntegerField(default=0, help_text='点击数', verbose_name='点击数'),
        ),
    ]
