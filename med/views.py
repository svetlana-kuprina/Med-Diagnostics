
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from datetime import datetime

from config import settings
from med.models import Doctors, Content, Category, Services, Appointment
from users.models import CustomUser


def home(request):
    """ "Главная страница"""
    content = Content.objects.first()
    categories = Category.objects.all()
    users = CustomUser.objects.all()
    return render(request, "home.html", {"content": content, "categories": categories, "users": users})


def doctors_list(request, pk):
    """Списки врачей по категориям"""
    category = get_object_or_404(Category, pk=pk)
    doctors = Doctors.objects.filter(category=category)  # Врачи в этой категории
    return render(request, "doctors_list.html", {"category": category, "doctors": doctors})


def category_detail(request, pk):
    """Списки услуг по категориям"""
    category = get_object_or_404(Category, pk=pk)
    services = Services.objects.filter(category=category)  # Услуги в этой категории
    doctors = Doctors.objects.filter(category=category)  # Врачи в этой категории
    return render(request, "category_detail.html", {"category": category, "services": services, "doctors": doctors})


def company(request):
    """О компании"""
    content = Content.objects.first()
    categories = Category.objects.all()
    return render(request, "company.html", {"content": content, "categories": categories})

def appointment_view(request):
    """Страница записи на приём"""
    categories = Category.objects.all()
    content = Content.objects.first()

    # Передаём данные для динамических списков
    services_data = {}
    doctors_data = {}

    for category in categories:
        services = Services.objects.filter(category=category)
        services_data[category.pk] = [{"pk": s.pk, "name": s.name, "price": s.price} for s in services]

        for service in services:
            doctors = service.doctors.all()
            if doctors:
                doctors_data[service.pk] = [{"pk": d.pk, "name": d.name, "position": d.position} for d in doctors]

    context = {
        "categories": categories,
        "content": content,
        "services_data": services_data,
        "doctors_data": doctors_data,
    }

    try:
        # Получаем данные
        service_id = request.POST.get("service")
        doctor_id = request.POST.get("doctor")
        date = request.POST.get("date")
        time = request.POST.get("time")
        comment = request.POST.get("comment", "")

        # Проверяем, что все обязательные поля заполнены
        if not all([service_id, doctor_id, date, time]):
            messages.error(request, "Пожалуйста, заполните все обязательные поля.")
            return render(request, "appointment.html", context)

        # Собираем дату и время
        naive_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        # Делаем datetime привязываем к текущему часовому поясу
        date_time = timezone.make_aware(naive_datetime)

        # Проверяем, что дата не в прошлом
        if date_time < timezone.now():
            messages.error(request, "Дата и время не могут быть в прошлом.")
            return render(request, "appointment.html", context)

        # Получаем объекты
        service = get_object_or_404(Services, pk=service_id)
        doctor = get_object_or_404(Doctors, pk=doctor_id)

        # Определяем владельца записи
        if request.user.is_authenticated:
            owner = request.user
            user_email = request.user.email
            user_name = request.user.get_full_name() or request.user.username


        # Создаём запись
        appointment = Appointment(
            owner=request.user if request.user.is_authenticated else None,
            doctor=doctor,
            service=service,
            date_time=date_time,
            status="active",
        )
        appointment.save()
        # Отправляем письмо с подтверждением
        try:
            if user_email:
                send_mail(
                    subject="Подтверждение записи на приём",
                    message=(
                        f"Здравствуйте, {user_name}!\n\n"
                        f"Вы успешно записались на приём в медицинский центр «МедДиагностика».\n\n"
                        f"Услуга: {service.name}\n"
                        f"Врач: {doctor.name}\n"
                        f"Дата и время: {date_time.strftime('%d.%m.%Y %H:%M')}\n"
                        f"Адрес: {content.address if content else 'ул. Диагностическая, д. 7'}\n\n"
                        f"Для отмены или изменения записи свяжитесь с нами по телефону.\n\n"
                        f"С уважением,\n"
                        f"Команда «МедДиагностика»"
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user_email],
                )
        except Exception as email_error:
            print(f"Ошибка отправки письма: {email_error}")


        messages.success(
            request,
            f"✅ Вы успешно записались на приём к {doctor.name} на {date_time.strftime('%d.%m.%Y %H:%M')}! "
            f"Подтверждение отправлено на ваш email.",
        )
        return redirect("med:home")

    except Exception as e:
        messages.error(request, f"❌ Произошла ошибка при создании записи: {str(e)}")
        return render(request, "appointment.html", context)
    


