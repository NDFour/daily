# Generated by Django 2.2 on 2020-06-01 16:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0008_auto_20200602_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_modefy_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 1, 16, 38, 22, 356532, tzinfo=utc), verbose_name='上次修改时间'),
        ),
        migrations.AlterField(
            model_name='article',
            name='article_pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 1, 16, 38, 22, 356506, tzinfo=utc), verbose_name='新建时间'),
        ),
    ]
