# Generated by Django 2.2 on 2020-06-01 16:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='babaili_jiaji',
            name='report_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 1, 16, 47, 48, 939029, tzinfo=utc), verbose_name='时间'),
        ),
        migrations.AlterField(
            model_name='books',
            name='book_pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 1, 16, 47, 48, 938185, tzinfo=utc), verbose_name='更新时间'),
        ),
    ]
