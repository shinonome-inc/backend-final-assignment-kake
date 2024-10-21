from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

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
    success_url = reverse_lazy('tweets:postlist')  # やることやったらここに移動
    fields = ['title', 'content']

    def form_valid(self, form):  # バリデーション通過時にオーバライドする
        # 作成されたツイートの投稿者を現在ログイン中のユーザにする
        form.instance.user = self.request.user
        return super().form_valid(form)  # 通常の処理に戻す


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'tweets/list.html'
    context_object_name = 'tweets'


class TweetDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "tweets/detail_tweet.html"


class TweetUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'tweets/edit_tweet.html'
    success_url = reverse_lazy('tweets:postlist')  # やることやったらここに移動


class TweetDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "tweets/delete_tweet.html"
    success_url = reverse_lazy('tweets:postlist')  # やることやったらここに移動
