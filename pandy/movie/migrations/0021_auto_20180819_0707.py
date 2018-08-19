# Generated by Django 2.1 on 2018-08-19 07:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0020_auto_20180819_0402'),
    ]

    operations = [
        migrations.CreateModel(
            name='adArticles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='标题')),
                ('picurl', models.CharField(max_length=255, verbose_name='图片URL')),
                ('url', models.CharField(max_length=255, verbose_name='文章URL')),
                ('canbuuse', models.IntegerField(verbose_name='是否可用')),
                ('tab', models.IntegerField(default=1, verbose_name='位置(1/2)')),
            ],
        ),
        migrations.AlterField(
            model_name='movie',
            name='v_pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 19, 7, 7, 53, 974237, tzinfo=utc), verbose_name='最后更新时间'),
        ),
    ]
