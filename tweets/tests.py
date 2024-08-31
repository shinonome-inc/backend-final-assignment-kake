from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class TestHomeView(TestCase):

    def setUp(self):
        self.url = reverse("tweets:home")

        # ユーザーを作成
        self.user = User.objects.create_user(username="tester", password="testpassword")

        # そのユーザーをログイン
        self.client.login(username="tester", password="testpassword")

    # リクエストの送信
    def test_success_get(self):

        response = self.client.get(self.url)
        # self.url = tweets/home
        # self.client = サーバーに対してリクエストをシミュレート

        self.assertEqual(response.status_code, 200)
        # assertEqual(A, B) = Aの結果とBが一致すれば成功
