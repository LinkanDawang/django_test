# Generated by Django 3.1.5 on 2021-02-26 04:49

import datetime
from django.db import migrations
import simplepro.components.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210226_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='create_time',
            field=simplepro.components.fields.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='update_time',
            field=simplepro.components.fields.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间'),
        ),
    ]