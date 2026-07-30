from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    patronymic = models.CharField(
        max_length=100, verbose_name="Отчество", help_text="Введите отчество", null=True, blank=True
    )
    email = models.EmailField(unique=True, verbose_name="email")

    telephone = models.CharField(
        max_length=20, verbose_name="Номер телефона", null=True, blank=True, help_text="Введите номер телефона"
    )
    token = models.CharField(max_length=100, unique=True, verbose_name="Token", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]

    def __str__(self):
        return self.email
