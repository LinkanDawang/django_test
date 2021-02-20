from django.urls import path, re_path

from . import views

app_name = "user"


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    re_path(r'active/(?P<token>.+)$', views.ActiveView.as_view(), name='active'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('login_json/', views.LoginJsonView.as_view(), name='login_json'),
    path('logout/', views.LogoutView.as_view(), name='logout')
]

