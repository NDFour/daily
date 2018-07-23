# Generated by Django 2.0.2 on 2018-07-19 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('v_name', models.CharField(max_length=100)),
                ('v_url', models.CharField(max_length=256)),
                ('v_pass', models.CharField(default='Not need', max_length=10)),
                ('v_pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
    ]
