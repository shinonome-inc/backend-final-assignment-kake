from django.contrib.auth.forms import AuthenticationForm

# 初期状態ではlogin_logoutにforms.pyはないため自分で作成する


# ログインフォーム
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
