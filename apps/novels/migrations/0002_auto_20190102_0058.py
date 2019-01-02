# Generated by Django 2.0 on 2019-01-01 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novel',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='novel', to='authors.NovelAuthor', verbose_name='作者'),
        ),
    ]