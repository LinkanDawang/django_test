# Generated by Django 3.1.5 on 2021-03-24 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_log', '0003_auto_20210323_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestlog',
            name='telco',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='电信运营商'),
        ),
    ]
