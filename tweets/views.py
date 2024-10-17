from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView

from .models import Post


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "tweets/home.html"
    from .models import Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user  # 現在ログインしているユーザーを渡す
        return context


class TweetCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'tweets/create_tweet.html'
    success_url = '/tweets/home/' 
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
