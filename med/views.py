from django.shortcuts import render, get_object_or_404

from med.models import Doctors, Content, Category, Services


def home(request):
    content = Content.objects.first()
    categories = Category.objects.all()
    return render(request, "home.html", {"content": content, "categories": categories})

def doctors_list(request):
    doctors = Doctors.objects.all()
    return render(request, "doctors_list.html", {"doctors": doctors})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    services = Services.objects.filter(category=category)  # Услуги в этой категории
    return render(request, "category_detail.html", {
        "category": category,
        "services": services
    })