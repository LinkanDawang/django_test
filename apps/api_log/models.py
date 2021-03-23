from django.db import models
from rest_framework_tracking.base_models import BaseAPIRequestLog


class RequestLog(BaseAPIRequestLog):
    IN = 1
    OUT = 2
    LOGTYPE_CHOICES = ((IN, "IN"), (OUT, "OUT"))
    request_id = models.UUIDField(null=True, blank=True, verbose_name='RequestId')
    log_type = models.SmallIntegerField(choices=LOGTYPE_CHOICES, verbose_name="响应/请求")
    device_model = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备型号')
    device_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备名称')
    ip_address = models.CharField(max_length=100, null=True, blank=True, verbose_name="IP归属地址")

    class Meta:
        verbose_name = verbose_name_plural = "请求记录"
        managed = True
        db_table = 'request_log'
