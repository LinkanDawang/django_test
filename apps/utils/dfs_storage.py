from django.conf import settings
from django.core.files import File
from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client, get_tracker_conf


class FastDfsStorage(Storage):
    """
    Usage:
    from django.core.files.storage import default_storage
    with open("file_name.file_type", "rb") as f:
        url = default_storage.save(f.name, f)
    """
    def __init__(self, client_conf=None, server_ip=None):
        self.client_conf = client_conf if client_conf else settings.FDFS_CLIENT_CONF
        self.server_ip = server_ip if server_ip else settings.FDFS_SERVER_IP

    def _open(self, name, mode="rb"):
        pass

    def _save(self, name, content):
        client = Fdfs_client(get_tracker_conf(self.client_conf))
        try:
            ret = client.upload_by_buffer(content, name)
        except Exception as e:
            print(e)
            raise e
        new_name = ret["Remote file_id"]
        return self.url(new_name.decode())

    def get_available_name(self, name, max_length=None):
        name = super(FastDfsStorage, self).get_available_name(name, max_length)
        return name.split(".")[-1]

    def exists(self, name):
        return False

    def url(self, name):
        return self.server_ip + name
