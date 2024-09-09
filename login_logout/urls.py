from django.conf.urls import url
from django.urls import path

from . import views

# 初期状態ではlogin_logoutにurls.pyはないため自分で作成する

app_name = "login_logout"
urlpatterns = [
    path("", views.TopView.as_view(), name="top"),
    path("home/", views.HomeView.as_view(), name="home"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
