# Generated by Django 2.1 on 2018-09-11 07:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0037_auto_20180911_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='v_pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 11, 7, 41, 43, 927519, tzinfo=utc), verbose_name='最后更新时间'),
        ),
    ]