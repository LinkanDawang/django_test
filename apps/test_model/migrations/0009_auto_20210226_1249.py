# Generated by Django 3.1.5 on 2021-02-26 04:49

import datetime
from django.db import migrations
import simplepro.components.fields


class Migration(migrations.Migration):

    dependencies = [
        ('test_model', '0008_auto_20210226_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='create_time',
            field=simplepro.components.fields.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='update_time',
            field=simplepro.components.fields.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='uploadfile',
            name='create_time',
            field=simplepro.components.fields.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='uploadfile',
            name='update_time',
            field=simplepro.components.fields.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间'),
        ),
    ]
