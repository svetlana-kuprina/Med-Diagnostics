import secrets

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect

from django.urls import reverse_lazy
from django.views.generic import CreateView

from config import settings
from users.forms import CustomUserCreationForm
from users.models import CustomUser


class RegisterView(CreateView):
    """Подтверждение почты"""

    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        """Отправка письма"""
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/activate/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Добрый день! Перейдите по ссылке для подтверждения почты: {url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return super().form_valid(form)


def email_verification_user(request, token):
    """Меняем статус пользователя"""
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    user.token = None
    user.save()

    return redirect(reverse_lazy("users:login"))
