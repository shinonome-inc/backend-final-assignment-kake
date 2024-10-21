from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]  # 'user'と'created_at'はフォームで入力しないため除外
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Enter the title"}),
            "content": forms.Textarea(attrs={"rows": 5, "placeholder": "Write your post content here"}),
        }
