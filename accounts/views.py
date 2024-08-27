from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy  # エラー1: reverse_lazyをインポート
from django.views.generic import CreateView

from .forms import SignupForm


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, username=username, password=password)  # エラー2: passwardをpasswordに修正
        if user is not None:  # エラー3: 認証成功時のみログインを実行
            login(self.request, user)
        return response
