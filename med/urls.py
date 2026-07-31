
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from med.apps import MedConfig
from med.views import home, category_detail

app_name = MedConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("category/<int:pk>/", category_detail, name="category_detail"),


]