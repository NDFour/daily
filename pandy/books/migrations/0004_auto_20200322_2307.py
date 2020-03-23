# Generated by Django 2.2.5 on 2020-03-22 15:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20200322_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='book_description',
            field=models.TextField(verbose_name='内容简介'),
        ),
        migrations.AlterField(
            model_name='books',
            name='book_pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 22, 15, 7, 14, 35754, tzinfo=utc), verbose_name='更新时间'),
        ),
    ]
