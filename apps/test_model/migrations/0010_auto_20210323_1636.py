# Generated by Django 3.1.5 on 2021-03-23 08:36

from django.db import migrations
import simplecus.components.fields


class Migration(migrations.Migration):

    dependencies = [
        ('test_model', '0009_auto_20210226_1249'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='uploadfile',
            options={'managed': True, 'verbose_name': '示例', 'verbose_name_plural': '示例'},
        ),
        migrations.AlterField(
            model_name='uploadfile',
            name='point',
            field=simplecus.components.fields.RateField(verbose_name='评分'),
        ),
    ]
