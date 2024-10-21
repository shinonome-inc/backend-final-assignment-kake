from django.conf import settings
from django.db import models


class Post(models.Model):
    # タイトル
    title = models.CharField(max_length=100)
    # 本文
    content = models.TextField()
    # 投稿者
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 投稿日時
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]  # 投稿順にクエリを取得
