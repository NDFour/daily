# Generated by Django 2.2.5 on 2020-03-22 13:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0056_auto_20200322_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='v_pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 22, 13, 20, 0, 558843, tzinfo=utc), verbose_name='最后更新时间'),
        ),
    ]
