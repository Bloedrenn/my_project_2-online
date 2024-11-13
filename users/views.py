from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from core.models import Visit
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from .forms import VisitUpdateForm


CABINET_MENU = [
    {'title': 'Все заявки', 'url': reverse_lazy('cabinet:all_visits'), 'icon': 'bi-list-ul', 'active': False},
    {'title': 'Новые заявки', 'url': reverse_lazy('cabinet:new_visits'), 'icon': 'bi-bell', 'active': False},
    {'title': 'Архив заявок', 'url': reverse_lazy('cabinet:visit_archive'), 'icon': 'bi-archive', 'active': False},
    {'title': 'Сменить пароль', 'url': reverse_lazy('cabinet:change_password'), 'icon': 'bi-key', 'active': False},
]
def get_cabinet_menu_context(current_url: str) -> dict:
    menu = []
    # Создаем новый список, а не модифицируем существующий
    for item in CABINET_MENU:
        menu.append({
            'title': item['title'],
            'url': item['url'],
            'icon': item['icon'],
            'active': item['url'] == current_url
        })
    return {"cabinet_menu": menu}


class LoginView(BaseLoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('cabinet:new_visits')
    redirect_authenticated_user = True


class LogoutView(BaseLogoutView):
    next_page = reverse_lazy('main')


class ProfileVisitsListView(LoginRequiredMixin, ListView):
    model = Visit
    template_name = 'visits_list.html'
    context_object_name = 'visits'
    
    def get_queryset(self):
        # Получаем тип визита из параметров URL
        visit_type = self.kwargs.get('visit_type')
        
        # Базовый queryset для всех визитов
        queryset = Visit.objects.all()
        
        # Фильтрация визитов в зависимости от типа и установка заголовка страницы
        if visit_type == 'new':
            queryset = queryset.filter(status=0)
            self.page_title = 'Новые заявки'
        elif visit_type == 'archive':
            queryset = queryset.filter(status__in=[2, 3])
            self.page_title = 'Архив заявок'
        else:
            self.page_title = 'Все заявки'
            
        return queryset
    
    def get_context_data(self, **kwargs):
        # Получаем базовый контекст от родительского класса
        context = super().get_context_data(**kwargs)
        # Добавляем заголовок страницы в контекст
        context['page_title'] = self.page_title
        # Добавляем контекст меню кабинета
        context.update(get_cabinet_menu_context(self.request.path))
        return context


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('cabinet:all_visits')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_cabinet_menu_context(self.request.path))
        return context
    

class VisitDetailView(LoginRequiredMixin, DetailView):
    model = Visit
    template_name = 'visit_detail.html'
    context_object_name = 'visit' # Можно без
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_cabinet_menu_context(self.request.path))
        return context
    
    
class VisitDeleteView(LoginRequiredMixin, DeleteView):
    model = Visit
    success_url = reverse_lazy('cabinet:all_visits')
    
    # Не работает (Нужен шаблон подтверждения)
    # def get(self, request, *args, **kwargs):
    #     return self.post(request, *args, **kwargs)


class VisitUpdateView(LoginRequiredMixin, UpdateView):
    model = Visit
    form_class = VisitUpdateForm
    template_name = 'visit_update.html'
    
    def get_success_url(self):
        return reverse_lazy('cabinet:visit_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_cabinet_menu_context(self.request.path))
        return context
