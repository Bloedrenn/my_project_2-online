from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from core.models import Visit
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from .forms import VisitUpdateForm, VisitCreateForm
from .forms import BootstrapAuthenticationForm


CABINET_MENU = [
    {'title': 'Создать заявку', 'url': reverse_lazy('cabinet:create_visit'), 'icon': 'bi-plus-circle', 'active': False},
    {'title': 'Новые заявки', 'url': reverse_lazy('cabinet:new_visits'), 'icon': 'bi-bell', 'active': False},
    {'title': 'Подтвержденные заявки', 'url': reverse_lazy('cabinet:all_visits'), 'icon': 'bi-list-ul', 'active': False},
    {'title': 'Архив заявок', 'url': reverse_lazy('cabinet:visit_archive'), 'icon': 'bi-archive', 'active': False},
    {'title': 'Сменить пароль', 'url': reverse_lazy('cabinet:change_password'), 'icon': 'bi-key', 'active': False},
]
def get_cabinet_menu_context(current_url: str) -> dict:
    menu = []
    # Получаем количество заявок для бейджей
    new_visits_count = Visit.objects.filter(status=0).count()
    confirmed_visits_count = Visit.objects.filter(status=1).count()
    
    # Формируем список пунктов меню на основе константы CABINET_MENU
    for item in CABINET_MENU:
        # Создаем словарь с параметрами для каждого пункта меню
        menu_item = {
            'title': item['title'],
            'url': item['url'],
            'icon': item['icon'],
            # Определяем активный пункт меню путем сравнения URL
            'active': item['url'] == current_url,
            'badge_count': 0  # По умолчанию счетчик 0
        }
        
        # Добавляем счетчики для соответствующих пунктов меню
        if item['url'] == reverse_lazy('cabinet:new_visits'):
            menu_item['badge_count'] = new_visits_count
        elif item['url'] == reverse_lazy('cabinet:all_visits'):
            menu_item['badge_count'] = confirmed_visits_count
            
        # Добавляем сформированный пункт меню в общий список
        menu.append(menu_item)
    
    # Возвращаем готовый контекст для шаблона
    return {"cabinet_menu": menu}


class LoginView(BaseLoginView):
    template_name = 'login.html'
    form_class = BootstrapAuthenticationForm
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
            queryset = queryset.filter(status=1)
            self.page_title = 'Подтвержденные заявки'
            
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


class VisitCreateView(LoginRequiredMixin, CreateView):
    model = Visit
    form_class = VisitCreateForm
    template_name = 'visit_create.html'
    success_url = reverse_lazy('cabinet:all_visits')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_cabinet_menu_context(self.request.path))
        return context


# Эксперимент
# from django.contrib.auth import logout
# from django.shortcuts import redirect
# from django.views import View

# class LogoutView(View):
#     """
#     Мы сознательно заменили спец. вью LogoutView на обычную
#     в рамках эксперимента выхода с сайта через get запрос
#     (по умолнчаию это только через POST происходит в LogoutView)
#     """
#     def get(self, request):
#         logout(request)
#         return redirect(reverse_lazy('main'))