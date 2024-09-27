from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import SignupForm

User = get_user_model()  # グローバル変数としてカスタムユーザーモデルを使用


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return response


class UserProfileView(LoginRequiredMixin, DetailView):

    template_name = "accounts/UserProfile.html"

    model = User  # クラス内でグローバル変数を使用

    # URLから'slug'（username）を使ってユーザーを取得する
    slug_field = "username"
    slug_url_kwarg = "username"
