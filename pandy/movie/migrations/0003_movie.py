# Generated by Django 2.0.2 on 2018-07-23 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('movie', '0002_delete_movie'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('v_href', models.CharField(max_length=255)),
                ('v_pic', models.CharField(max_length=255)),
                ('v_name', models.CharField(max_length=255)),
                ('v_bdpan', models.CharField(max_length=255)),
                ('v_pass', models.CharField(max_length=255)),
                ('v_ed2k', models.CharField(max_length=255)),
                ('v_magnet', models.CharField(max_length=255)),
            ],
        ),
    ]
