from django.db import models

from users.models import CustomUser


class Category(models.Model):
    """Модель: Категории услуг"""

    name = models.CharField(
        max_length=150, verbose_name="Наименование категории услуг", help_text="Введите наименование категории"
    )
    description = models.TextField(
        null=True, blank=True, verbose_name="Описание категории услуг", help_text="Введите описание"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория услуг"
        verbose_name_plural = "Категории услуг"
        ordering = ["name"]


class Doctors(models.Model):
    """Модель: Информация по врачам"""

    name = models.CharField(max_length=150, verbose_name="ФИО", help_text="Введите фамилию имя и отчество врача")
    position = models.CharField(
        max_length=150, null=True, blank=True, verbose_name="Должность", help_text="Введите должность врача"
    )
    experience = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Стаж", help_text="Введите стаж работы"
    )
    photo = models.ImageField(
        upload_to="static/photo/",
        null=True,
        blank=True,
        verbose_name="Фото доктора",
        help_text="Загрузите фото доктора",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="doctors",
        verbose_name="Категория",
        help_text="Выберите категорию",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Информация по врачам"
        verbose_name_plural = "Информации по врачам"
        ordering = ["name"]


class Services(models.Model):
    """Модель: Услуги"""

    name = models.CharField(
        max_length=150, verbose_name="Наименование услуги", help_text="Введите наименование услуги"
    )
    description = models.TextField(
        null=True, blank=True, verbose_name="Описание услуги", help_text="Введите описание услуги"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="services",
        verbose_name="Категория",
        help_text="Выберите категорию",
    )
    doctors = models.ManyToManyField(Doctors, null=True, blank=True, related_name="services")
    price = models.FloatField(verbose_name="Цена", help_text="Введите цену услуги")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["name"]


class Appointment(models.Model):
    """Модель: Запись на прием"""

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="owner_client",
        verbose_name="Владелец",
        blank=True,
        null=True,
    )
    doctor = models.ForeignKey(Doctors, on_delete=models.SET_NULL, null=True, blank=True, related_name="doctor_client")
    service = models.ForeignKey(Services, on_delete=models.SET_NULL, null=True, blank=True, related_name="services")
    date_time = models.DateTimeField(verbose_name="Дата и время записи на прием")
    STATUS_CHOICES = [
        ("active", "Активна"),
        ("cancelled", "Отменена"),
        ("completed", "Исполнена"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active", verbose_name="Статус")
    result = models.TextField(
        null=True, blank=True, verbose_name="Результат диагностики", help_text="Введите результат диагностики"
    )

    def __str__(self):
        return f"Запись на прием: {self.owner} - {self.date_time}"

    class Meta:
        verbose_name = "Запись на прием"
        verbose_name_plural = "Записи на прием"
        ordering = ["owner", "date_time", "status"]


class Content(models.Model):
    name = models.CharField(
        max_length=150, verbose_name="Наименование организации", help_text="Введите наименование организации"
    )
    photo = models.ImageField(
        upload_to="static/photo/",
        null=True,
        blank=True,
        verbose_name="Фото организации",
        help_text="Загрузите фото организации",
    )
    description = models.TextField(
        null=True, blank=True, verbose_name="Описание организации", help_text="Введите описание организации"
    )
    history = models.TextField(null=True, blank=True, verbose_name="История", help_text="Введите историю организации")
    mission = models.TextField(
        null=True, blank=True, verbose_name="Миссия и ценности", help_text="Введите миссию и ценности организации"
    )
    address = models.TextField(
        null=True, blank=True, verbose_name="Адрес организации", help_text="Введите адрес организации"
    )
    email = models.EmailField(unique=True, verbose_name="email организации")

    telephone = models.CharField(
        max_length=20,
        verbose_name="Номер телефона",
        null=True,
        blank=True,
        help_text="Введите номер телефона организации",
    )
    operating_mode = models.CharField(
        max_length=150, verbose_name="Режим работы (кратко)", help_text="Введите режим работы организации"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Управление контентом сайта"
        verbose_name_plural = "Управление контентом сайта"
        ordering = ["name"]
