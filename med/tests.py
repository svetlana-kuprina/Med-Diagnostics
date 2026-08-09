from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from med.models import Content, Category, Doctors, Services, Appointment
from users.models import CustomUser


class MedTests(TestCase):
    """Тест доступа на сайт"""

    def setUp(self):
        # Создаём пользователя
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@test.ru",
            password="testpassword123",
            first_name="Тест",
            last_name="Тест",
            patronymic="Тест",
            telephone="+7 (999) 999-99-99",
        )
        # Создаём данные организации
        test_image = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg",
        )
        self.content = Content.objects.create(
            name="МедДиагностикаТест",
            photo=test_image,
            description="Тестовое описание",
            address="ул. Тестовая, д. 1",
            email="info@test.ru",
            telephone="+7 (999) 999-99-99",
            operating_mode="Пн-Вс 8:00-20:00",
        )

        # Создаём категорию
        self.category = Category.objects.create(name="Тестовая категория", description="Тестовое описание категории")

        # Создаём врача
        self.doctor = Doctors.objects.create(
            name="Тестов Тест Тестович", position="Тестовый врач", experience="10 лет", category=self.category
        )

        # Создаём услугу
        self.service = Services.objects.create(
            name="Тестовая услуга", description="Тестовое описание услуги", category=self.category, price=1000.00
        )
        # Создаём запись на прием
        self.appointment = Appointment.objects.create(
            owner=self.user,
            doctor=self.doctor,
            service=self.service,
            date_time=timezone.now(),
            status="active",
        )
    def test_med_home(self):
        """Тест главной страницы"""
        url = reverse("med:home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_authenticated_user(self):
        """Тест главной страницы для авторизованного пользователя"""
        self.client.login(email="test@test.ru", password="testpassword123")
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

    def test_appointment_no_authenticated_user(self):
        """Тест ограничения доступа страницы Личный кабинет пользователя"""
        response = self.client.get(reverse("med:profile"))
        self.assertEqual(response.status_code, 302)

    def test_appointment_authenticated_user(self):
        """Тест доступа страницы Личный кабинет пользователя"""
        self.client.login(email="test@test.ru", password="testpassword123")
        response = self.client.get(reverse("med:profile"))
        self.assertEqual(response.status_code, 200)

    def test_appointment_page(self):
        """Тест запроса страницы записи"""
        response = self.client.get(reverse("med:appointment"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.appointment.service, self.service)
        self.assertEqual(self.appointment.doctor, self.doctor)
    
    def test_appointment_status(self):
        """Тест смены статуса при отмене записи"""
        self.client.login(email="test@test.ru", password="testpassword123")
        response = self.client.get(reverse("med:cancel_appointment_confirm", args=[self.appointment.pk]))
        self.assertEqual(response.status_code, 302)
        self.appointment.refresh_from_db()
        self.assertTrue(self.appointment.status=="cancelled")
       
    def tearDown(self):
        pass
