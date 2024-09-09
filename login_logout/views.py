from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

from . import forms


class TopView(TemplateView):
    template_name = "login_logout/top.html"


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "login_logout/home.html"


class LiginView(LoginView):  # ログインページ
    form_class = forms.LoginForm
    template_name = "login_logout/login.html"


class LogoutView(LoginRequiredMixin, LogoutView):  # ログアウトページ
    template_name = "login_logout/logout.html"
