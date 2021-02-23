from qiniu import Auth, put_file, etag
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.storage import Storage
from django.conf import settings


class QiniuStorage(Storage):
    location = settings.STATIC_ROOT + '/'
    client = Auth(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def exists(self, name):
        self.generate_filename()
        return False

    def url(self, name):
        return settings.AWS_S3_ENDPOINT_URL + name

    def _save(self, name, content):
        token = self.client.upload_token(self.bucket_name, name, 3600)
        file_path = self.location + name
        ret, info = put_file(token, name, file_path)
        assert ret['key'] == name
        # assert ret['hash'] == etag(content)
