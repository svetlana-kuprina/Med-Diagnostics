from django.urls import path

from med.apps import MedConfig
from med.views import (
    home,
    category_detail,
    company,
    doctors_list,
    appointment_view,
    ProfileListView,
    cancel_appointment_confirm,
    cancel_appointment,
    feedback,
)

app_name = MedConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("category/<int:pk>/", category_detail, name="category_detail"),
    path("company", company, name="company"),
    path("doctors_list/<int:pk>/", doctors_list, name="doctors_list"),
    path("appointment/", appointment_view, name="appointment"),
    path("profile/", ProfileListView.as_view(), name="profile"),
    path("cancel_appointment/<int:pk>/", cancel_appointment, name="cancel_appointment"),
    path('cancel_appointment_confirm/<int:pk>/', cancel_appointment_confirm, name='cancel_appointment_confirm'),
    path("feedback/", feedback, name="feedback"),
]
