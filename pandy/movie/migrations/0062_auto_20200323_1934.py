# Generated by Django 2.2 on 2020-03-23 11:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0061_auto_20200323_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='v_pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 23, 11, 34, 38, 374623, tzinfo=utc), verbose_name='最后更新时间'),
        ),
    ]