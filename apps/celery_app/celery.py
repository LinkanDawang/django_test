import os
from datetime import timezone

from celery import Celery
from django.apps import AppConfig

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.local"

app = Celery("django-test")


class CeleryConfig(AppConfig):
    name = "apps.celery_app"
    verbose_name = "Celery Config"

    def read(self):
        app.config_from_object('django.conf:settings', namespace='CELERY')
        # 解决时区问题,定时任务启动就循环输出
        app.now = timezone.now
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)
