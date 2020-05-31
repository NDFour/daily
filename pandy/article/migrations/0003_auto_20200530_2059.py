# Generated by Django 2.2.5 on 2020-05-30 12:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20200530_2039'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='_type',
            new_name='article_type',
        ),
        migrations.AlterField(
            model_name='article',
            name='article_pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 30, 12, 59, 36, 270153, tzinfo=utc), verbose_name='更新时间'),
        ),
    ]