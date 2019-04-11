from apps.utils.model import BaseModel
from django.conf import settings

from django.db import models
from django.contrib.auth.models import AbstractUser

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# Create your models here.


class Users(AbstractUser, BaseModel):
    """用户"""
    cell_phone = models.CharField(max_length=11, blank=True, verbose_name='手机号码')

    class Meta:
        db_table = 't_users'

    def generate_activate_token(self):
        """生成激活令牌"""
        serializer = Serializer(settings.SECRET_KEY, 3600)
        token = serializer.dumps({'confirm': self.id})

        return token

