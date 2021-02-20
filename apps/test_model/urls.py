from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from .views import IndexView, TestDRFViewSet

app_name = "test"
router = DefaultRouter()

urlpatterns = [
    path('test/', view=IndexView.as_view(), name='aaaaaa'),
]
router.register(r"drf", TestDRFViewSet)

urlpatterns += router.urls
