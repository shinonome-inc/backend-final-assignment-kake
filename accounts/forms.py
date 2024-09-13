from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
)  # 「AuthenticationForm」クラスはユーザーログインのためにフォーム
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()  # こっちで先に変数代入する！


class SignupForm(UserCreationForm):
    class Meta:
        model = User  # model = get_user_model() は NG
        fields = ("username", "email")


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["placeholder"] = field.label
            # 全てのフォームの部品にplaceholderを定義して、入力フォームにフォーム名が表示されるように指定する
