# Generated by Django 3.1.5 on 2021-02-26 03:41

from django.db import migrations
import simplepro.components.fields


class Migration(migrations.Migration):

    dependencies = [
        ('test_model', '0005_auto_20210226_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfile',
            name='create_time',
            field=simplepro.components.fields.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='uploadfile',
            name='state',
            field=simplepro.components.fields.RadioField(choices=[(0, '无效'), (1, '有效')], default=0, help_text='只能选一个', verbose_name='单选框'),
        ),
        migrations.AlterField(
            model_name='uploadfile',
            name='update_time',
            field=simplepro.components.fields.DateTimeField(auto_now=True, verbose_name='创建时间'),
        ),
    ]