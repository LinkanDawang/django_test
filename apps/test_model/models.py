from django.db import models
from apps.utils.model import BaseModel, VirtualForeignKey
from django.contrib.postgres.fields import JSONField

# from django.contrib.auth.models import User
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType


class TestModel(models.Model):
    conf = models.CharField(max_length=50, null=True, blank=True, verbose_name='联系人信息')

    class Meta:
        verbose_name = verbose_name_plural = '表'
        db_table = "test_table"


class Supplier(BaseModel):
    name = models.CharField(max_length=128, null=True, blank=True, verbose_name="名称")
    fname = models.CharField(max_length=128, null=True, blank=True, verbose_name="简称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "供应商表"
        managed = True
        db_table = "supplier"
