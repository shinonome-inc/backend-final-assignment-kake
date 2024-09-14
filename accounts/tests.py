from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import TestCase
from django.urls import reverse

from mysite import settings

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
            reverse("accounts:UserProfile"),
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

    # フォーム未入力でリクエストの送信
    def test_failure_post_with_empty_form(self):
        invalid_data = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }

        response = self.client.post(self.url, invalid_data)

        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["username"])
        self.assertIn("このフィールドは必須です。", form.errors["email"])
        self.assertIn("このフィールドは必須です。", form.errors["password1"])
        self.assertIn("このフィールドは必須です。", form.errors["password2"])

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

    # すでに存在するユーザ名での登録
    def test_failure_post_with_duplicated_user(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        # テストユーザの作成
        self.User = get_user_model()
        self.existing_user = self.User.objects.create_user(username="testuser", password="testpassword")

        response = self.client.post(self.url, invalid_data)

        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn("同じユーザー名が既に登録済みです。", form.errors["username"])

    # 無効なメールアドレスでのリクエストの送信
    def test_failure_post_with_invalid_email(self):
        invalid_data = {
            "username": "testuser",
            "email": "testmail",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, invalid_data)

        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("有効なメールアドレスを入力してください。", form.errors["email"])

    # 短すぎるパスワードでのリクエストの送信
    def test_failure_post_with_short_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "testmail",
            "password1": "test",
            "password2": "test",
        }

        response = self.client.post(self.url, invalid_data)

        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        # self.assertIn("このパスワードは短すぎます。最低 8 文字以上必要です。", form.errors["password1"])
        # form.errorsの中に'password1'というキーが存在しない可能性がある
        self.assertIn("このパスワードは短すぎます。最低 8 文字以上必要です。", form.errors["password2"])

    # ユーザネームと類似したパスワードでのリクエストの送信
    def test_failure_post_with_password_similar_to_username(self):
        invalid_data = {
            "username": "testuser",
            "email": "testmail",
            "password1": "testuser",
            "password2": "testuser",
        }

        response = self.client.post(self.url, invalid_data)

        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        # self.assertIn("このパスワードは ユーザー名 と似すぎています。", form.errors["password1"])
        # form.errorsの中に'password1'というキーが存在しない可能性がある
        self.assertIn("このパスワードは ユーザー名 と似すぎています。", form.errors["password2"])

    # パスワードがすべて数字でのリクエストの送信
    def test_failure_post_with_only_numbers_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "testmail",
            "password1": "12345678",
            "password2": "12345678",
        }

        response = self.client.post(self.url, invalid_data)

        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        # self.assertIn("このパスワードは数字しか使われていません。", form.errors["password1"])
        # form.errorsの中に'password1'というキーが存在しない可能性がある
        self.assertIn("このパスワードは数字しか使われていません。", form.errors["password2"])

    #  password1とpassword2が異なる状態でのリクエストの送信
    def test_failure_post_with_mismatch_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "testmail",
            "password1": "testpassword",
            "password2": "testpassward",
        }

        response = self.client.post(self.url, invalid_data)

        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("確認用パスワードが一致しません。", form.errors["password2"])
        # 「確認用パスワードが一致しません。」などのエラー文は少しでも間違えるとテストでエラーが出るので気を付けること


class TestLoginView(TestCase):
    def setUp(self):
        self.url = reverse(settings.LOGIN_URL)
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        valid_login_data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post(self.url, valid_login_data)
        self.assertRedirects(
            response,
            reverse(settings.LOGIN_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_not_exists_user(self):
        invalid_login_data = {
            "username": "nonexistinguser",
            "password": "testpassword",
        }
        response = self.client.post(self.url, invalid_login_data)
        form = response.context["form"]
        self.assertIn(
            "正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。",
            form.errors["__all__"],
        )

    def test_failure_post_with_empty_password(self):
        invalid_login_data = {
            "username": "testuser",
            "password": "",
        }
        response = self.client.post(self.url, invalid_login_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertIn("このフィールドは必須です。", form.errors["password"])


class TestLogoutView(TestCase):

    def setUp(self):
        # ユーザーを作成しログイン
        self.user = User.objects.create_user(username="testuser", password="testpassword123")
        self.client.login(username="testuser", password="testpassword123")
        # ログアウト用の URL を逆引きして保存
        self.logout_url = reverse("accounts:logout")

    def test_success_post(self):
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, "/accounts/login/")
