# Generated by Django 3.1.5 on 2021-02-25 09:42

from django.db import migrations, models
import simplecus.components.fields


class Migration(migrations.Migration):

    dependencies = [
        ('test_model', '0003_uploadfile_file_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfile',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='upload/', verbose_name='上传文件'),
        ),
        migrations.AlterField(
            model_name='uploadfile',
            name='file_icon',
            field=simplecus.components.fields.ImageField(blank=True, max_length=128, null=True, verbose_name='图片上传'),
        ),
    ]
