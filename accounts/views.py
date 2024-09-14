from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin  # 「LoginRequiredMixin」クラスはログインを必須にするためのもの
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import LoginForm, SignupForm


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return response


class Login(LoginView):
    form_class = LoginForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("accounts:UserProfile")


class UserProfileView(LoginRequiredMixin, TemplateView):
    login_url = "/login/"
    template_name = "registration/UserProfile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.request.user.username
        return context
