from django.shortcuts import render, redirect
from .forms import VisitModelForm, ReviewModelForm
from .models import Visit, Master, Service, Review
from django.http import JsonResponse
from django.views.generic import (
    View,
    TemplateView,
    FormView,
    CreateView,
    DetailView,
    UpdateView,
    ListView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


MENU = [
        {'title': 'Главная', 'url': '/', 'active': True},
        {'title': 'Мастера', 'url': '#masters', 'active': True},
        {'title': 'Услуги', 'url': '#services', 'active': True},
        {'title': 'Отзывы', 'url': '#reviews', 'active': True},
        {'title': 'Оставить отзыв', 'url': reverse_lazy('review_create'), 'active': True},
        {'title': 'Запись на стрижку', 'url': '#orderForm', 'active': True},
    ]

def get_menu_context(menu: list[dict] = MENU):
    return {"menu": menu}


class MainView(View):
    """
    Метод get - отвечает за запросы GET
    Есть еще и другие методы, например post, put, delete и т.д.
    """
    
    def get(self, request):
        menu = get_menu_context()
        form = VisitModelForm()
        masters = Master.objects.all()
        published_reviews = Review.objects.filter(status=3)
        return render(request, "main.html", {"form": form, "masters": masters, "published_reviews": published_reviews, **menu})
    
    def post(self, request):
        form = VisitModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("thanks")
        # Отдаем заполненную форму с ошибку
        if form.errors:
            return render(
                request,
                "main.html",
                {"form": form, "masters": Master.objects.all(), **get_menu_context()},
            )
        

class ServicesByMasterView(View):
    def get(self, request, master_id):
        services = Master.objects.get(id=master_id).services.all()
        services_data = [
            {"id": service.id, "name": service.name} for service in services
        ]
        return JsonResponse({"services": services_data})
    

class ThanksTemplateView(TemplateView):
    template_name = "thanks.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_menu_context())
        return context
    

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewModelForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('review_thanks')
    extra_context = get_menu_context()


class ReviewThanksTemplateView(TemplateView):
    template_name = "review_thanks.html"
    extra_context = get_menu_context()
