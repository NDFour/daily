# Generated by Django 2.1 on 2018-09-11 09:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('onlineplay', '0009_auto_20180911_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlineplay',
            name='v_pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 11, 9, 22, 31, 395865, tzinfo=utc), verbose_name='更新时间'),
        ),
    ]
