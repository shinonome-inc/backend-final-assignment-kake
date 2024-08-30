from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class TestSignupView(TestCase):

    def setUp(self):
        self.url = reverse("accounts:signup")

    # リクエストの送信
    def test_success_get(self):

        response = self.client.get(self.url)
        # self.url = accounts/signup
        # self.client = サーバーに対してリクエストをシミュレート

        self.assertEqual(response.status_code, 200)
        # assertEqual(A, B) = Aの結果とBが一致すれば成功

        self.assertTemplateUsed(response, "accounts/signup.html")
        # assertTemplateUsed(A, B) = Aの結果とBが一致すれば成功

    # email, username, password1, password2を設定したデータでリクエストの送信
    def test_success_post(self):
        valid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        # ユーザーがフォームにデータを打ち込んでユーザー登録ボタンを押した操作を表している
        response = self.client.post(self.url, valid_data)  # エラー2 valid_date > valid_data に変更

        # 1の確認 = tweets/homeにリダイレクトすること
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )

        # 2の確認 = ユーザーが作成されること
        self.assertTrue(
            User.objects.filter(username=valid_data["username"]).exists()  # エラー1 userame > username に変更
        )

        # 3の確認 = ログイン状態になること
        self.assertIn(SESSION_KEY, self.client.session)
        # self.assertIn(A, B) = AがBに含まれているか

    # usernameを設定してないデータでリクエストの送信
    def test_failure_post_with_empty_username(self):
        invalid_data = {
            "username": "",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, invalid_data)

        form = response.context["form"]  # エラー1 content > context に変更

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username=invalid_data["username"]).exists()  # エラー2 fiter > filter に変更
        )
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["username"])

    # emailを設定してないデータでリクエストの送信
    def test_failure_post_with_empty_email(self):
        invalid_data = {
            "username": "testuser",
            "email": "",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, invalid_data)

        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["email"])

    # passwordを設定してないデータでリクエストの送信
    def test_failure_post_with_empty_passward(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "",
            "password2": "",
        }

        response = self.client.post(self.url, invalid_data)

        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["password1"])
        self.assertIn("このフィールドは必須です。", form.errors["password2"])
