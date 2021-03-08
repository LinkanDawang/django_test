from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class MyStorage(S3Boto3Storage):
    def _normalize_name(self, name):
        """
        处理文件名
        :param name:
        :return:
        """
        # FIXME simplePro中admin的模板里有很多填充静态资源的路径为绝对路径
        # FIXME 例: <link rel="stylesheet" href="{% static '/admin/simpleui-x/css/login.css' %}?_=2.1">
        # FIXME 问题：会导致storages.utils.safe_join抛出异常
        name = name[1:] if name.startswith("/") else name
        return super(MyStorage, self)._normalize_name(name)


class StaticStorage(MyStorage):
    location = settings.STATICFILES_LOCATION
    file_overwrite = True


class MediaStorage(MyStorage):
    location = settings.MEDIAFILES_LOCATION
    file_overwrite = True
