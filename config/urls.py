from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import url
from django.conf import settings
from django.views.generic import TemplateView

from apps.test_model.views import WatchGtViewSet


apipatterns = [
    path("main/", include('apps.test_model.urls', namespace="test")),  # test模块
    path("user/", include('apps.user.urls', namespace="user"))  # 用户模块
]

urlpatterns = [
    path('Watch/', WatchGtViewSet.as_view(actions={'get': 'list'}), name="Watch"),
    path('admin/', admin.site.urls),
    # path(r"_nested_admin/", include("nested_admin.urls")),
    path('api/', include(apipatterns)),
    re_path('^$', TemplateView.as_view(template_name="index.html"), name='account'),
]

if settings.ENV_NAME == "local":
    urlpatterns.append(
        path("silk/", include("silk.urls", namespace='silk'))
    )

