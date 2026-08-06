from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser


class MedTests(TestCase):
    """Тест доступа на сайт"""

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@test.ru",
            password="testpassword123",
            first_name="Тест",
            last_name="Тест",
            patronymic="Тест",
            telephone="+7 (999) 999-99-99",
        )

    def test_med_home(self):
        """Тест главной страницы"""
        url = reverse("med:home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_authenticated_user(self):
        """Тест главной страницы для авторизованного пользователя"""
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(reverse("med:home"))
        self.assertEqual(response.status_code, 200)

    def test_company_url(self):
        """Тест URL страницы о компании"""
        url = reverse("med:company")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_appointment(self):
        """Тест URL страницы записи на прием"""
        url = reverse("med:appointment")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass
