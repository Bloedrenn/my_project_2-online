from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Visit, Review, Master, Service


class Command(BaseCommand):
    help = 'Настройка начальных данных для проекта'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        # Создаем суперпользователя
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='ad@ad.ru',
                password='admin'
            )
            self.stdout.write(self.style.SUCCESS('Суперпользователь создан'))

        # Создаем группу Менеджер
        manager_group, created = Group.objects.get_or_create(name='Менеджер')
        
        # Получаем content type для каждой модели
        visit_content_type = ContentType.objects.get_for_model(Visit)
        review_content_type = ContentType.objects.get_for_model(Review)
        master_content_type = ContentType.objects.get_for_model(Master)
        service_content_type = ContentType.objects.get_for_model(Service)

        # Права для заявок (просмотр, редактирование, создание)
        visit_view = Permission.objects.get(content_type=visit_content_type, codename='view_visit')
        visit_change = Permission.objects.get(content_type=visit_content_type, codename='change_visit')
        visit_add = Permission.objects.get(content_type=visit_content_type, codename='add_visit')

        # Право только на просмотр отзывов
        review_view = Permission.objects.get(content_type=review_content_type, codename='view_review')

        # Право только на просмотр мастеров
        master_view = Permission.objects.get(content_type=master_content_type, codename='view_master')

        # Право только на просмотр услуг
        service_view = Permission.objects.get(content_type=service_content_type, codename='view_service')

        # Добавляем все права группе
        manager_group.permissions.add(
            visit_view,
            visit_change,
            visit_add,
            review_view,
            master_view,
            service_view
        )
        
        self.stdout.write(self.style.SUCCESS('Группа "Менеджер" создана и настроена'))
        
        # Добавляем админа в группу менеджеров
        admin_user = User.objects.get(username='admin')
        admin_user.groups.add(manager_group)
        self.stdout.write(self.style.SUCCESS('Админ добавлен в группу "Менеджер"'))
