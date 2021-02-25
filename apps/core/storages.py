from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    file_overwrite = True
    
    def _normalize_name(self, name):
        """
        处理文件名
        :param name:
        :return:
        """
        name = super(StaticStorage, self)._normalize_name(name)
        return name
