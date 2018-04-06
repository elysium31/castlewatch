# Generated by Django 2.0.4 on 2018-04-06 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180406_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_pages', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
    ]