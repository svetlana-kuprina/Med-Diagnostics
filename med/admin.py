from django.contrib import admin

from .models import Category, Services, Doctors, Appointment, Content


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    list_filter = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    
@admin.register(Doctors)
class DoctorsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "position", "category")
    list_filter = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "owner")
    list_filter = ("owner",)
    search_fields = ("owner",)
    ordering = ("owner",)

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
