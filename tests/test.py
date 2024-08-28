from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class TestSignupView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_success_post(self):
        valid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, valid_data)
        self.assertRedirects(response, reverse("tweets:home"), status_code=302)
        self.assertTrue(User.objects.filter(username=valid_data["username"]).exists())
        self.assertIn("_auth_user_id", self.client.session)

    def test_failure_post_with_empty_form(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "username", "このフィールドは必須です。")

    def test_failure_post_with_empty_username(self):
        invalid_data = {
            "username": "",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "username", "このフィールドは必須です。")

    def test_failure_post_with_empty_email(self):
        invalid_data = {
            "username": "testuser",
            "email": "",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "email", "このフィールドは必須です。")

    def test_failure_post_with_empty_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "password1", "このフィールドは必須です。")

    def test_failure_post_with_duplicated_user(self):
        User.objects.create_user(username="testuser", email="test@test.com", password="testpassword")
        invalid_data = {
            "username": "testuser",
            "email": "test2@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "username", "同じユーザー名が既に登録されています。")

    def test_failure_post_with_invalid_email(self):
        invalid_data = {
            "username": "testuser",
            "email": "invalid-email",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "email", "有効なメールアドレスを入力してください。")

    def test_failure_post_with_too_short_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "short",
            "password2": "short",
        }
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "password1", "このパスワードは短すぎます。")

    def test_failure_post_with_password_similar_to_username(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testuser123",
            "password2": "testuser123",
        }
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "password1", "このパスワードはユーザー名に似すぎています。")

    def test_failure_post_with_only_numbers_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "12345678",
            "password2": "12345678",
        }
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "password1", "このパスワードは数字しか含まれていません。")

    def test_failure_post_with_mismatch_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword1",
            "password2": "testpassword2",
        }
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "password2", "確認用パスワードが一致しません。")


class TestHomeView(TestCase):
    def setUp(self):
        self.url = reverse("tweets:home")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
