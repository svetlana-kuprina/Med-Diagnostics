from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from users.models import CustomUser  # Или из вашего приложения


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации с дополнительными полями модели CustomUser"""

    # Дополнительные поля для валидации
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    patronymic = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    telephone = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = CustomUser
        fields = ("email", "username", "first_name", "last_name", "patronymic", "telephone", "password1", "password2")

    def clean_email(self):
        """Проверка уникальности email"""
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean_telephone(self):
        """Опциональная валидация телефона"""
        telephone = self.cleaned_data.get("telephone")
        if telephone and len(telephone) < 5:
            raise ValidationError("Номер телефона слишком короткий.")
        return telephone

    def save(self, commit=True):
        """Сохранение пользователя со всеми полями"""
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        user.patronymic = self.cleaned_data.get("patronymic", "")
        user.telephone = self.cleaned_data.get("telephone", "")

        if commit:
            user.save()
        return user
