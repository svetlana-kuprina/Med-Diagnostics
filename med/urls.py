
from django.urls import path

from med.apps import MedConfig
from med.views import home, category_detail, company, doctors_list, appointment_view

app_name = MedConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("category/<int:pk>/", category_detail, name="category_detail"),
    path("company", company, name="company"),
    path("doctors_list/<int:pk>/", doctors_list, name="doctors_list"),
    path('appointment/', appointment_view, name='appointment'),


]