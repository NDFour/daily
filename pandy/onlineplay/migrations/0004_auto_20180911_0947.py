# Generated by Django 2.1 on 2018-09-11 01:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('onlineplay', '0003_auto_20180909_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='onlineplay',
            name='v_type',
            field=models.PositiveIntegerField(default=1, verbose_name='类型'),
        ),
        migrations.AddField(
            model_name='onlineplay',
            name='v_vip',
            field=models.IntegerField(default=0, verbose_name='vip视频'),
        ),
        migrations.AlterField(
            model_name='onlineplay',
            name='v_pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 11, 1, 47, 21, 211545, tzinfo=utc), verbose_name='更新时间'),
        ),
    ]