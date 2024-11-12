from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)  # Регистрация модели CustomUser в админ-панели Django
class CustomUserAdmin(UserAdmin):
    # Добавление дополнительного поля avatar к стандартным полям UserAdmin
    # Это позволит редактировать аватарку пользователя в админ-панели
    fieldsets = UserAdmin.fieldsets + (('Another', {'fields': ('avatar',)}),)
