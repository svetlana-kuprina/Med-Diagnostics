from django.core import mail
from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser


class MedUserTests(TestCase):
    """Тесты авторизации и создания пользователя"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.register_url = reverse("users:register")
        self.login_url = reverse("users:login")

        self.user_data = {
            "username": "testuser",
            "email": "test@test.ru",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "first_name": "Тест",
            "last_name": "Тест",
            "patronymic": "Тест",
            "telephone": "+7 (999) 999-99-99",
        }

    def test_login_page(self):
        """Тест проверки входа"""
        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        self.assertContains(response, "Вход в личный кабинет")

    def test_register_sends_email_and_activates_user(self):
        """Тест отправки письма подтверждения и активации пользователя"""
        # Отправляем POST запрос на регистрацию
        response = self.client.post(self.register_url, self.user_data)

        # Проверяем, что пользователь создан в БД
        self.assertEqual(CustomUser.objects.count(), 1)
        user = CustomUser.objects.first()

        # Проверяем правильность данных пользователя
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@test.ru")
        self.assertEqual(user.first_name, "Тест")
        self.assertEqual(user.last_name, "Тест")
        self.assertEqual(user.patronymic, "Тест")
        self.assertEqual(user.telephone, "+7 (999) 999-99-99")

        # Проверяем, что пользователь неактивен до подтверждения
        self.assertFalse(user.is_active)
        self.assertIsNotNone(user.token)

        # Проверяем, что отправлено письмо
        self.assertEqual(len(mail.outbox), 1)

        # Проверяем содержимое письма
        email = mail.outbox[0]
        self.assertEqual(email.subject, "Подтверждение почты")
        self.assertEqual(email.to, ["test@test.ru"])

        # Переходим по ссылке подтверждения
        activate_url = reverse("users:activate", kwargs={"token": user.token})
        self.client.get(activate_url)

        # Проверяем, что пользователь стал активным и токен удален, первая строка обновляет объект модели
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertIsNone(user.token)
