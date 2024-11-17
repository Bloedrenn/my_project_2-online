from django.contrib import admin
from .models import Visit, Master, Service, Review
from django.utils.html import format_html


class TimeOfDayFilter(admin.SimpleListFilter):
    title = 'Время суток'  # Отображаемое название фильтра
    parameter_name = 'time_of_day'  # URL параметр

    def lookups(self, request, model_admin):
        return (
            ('morning', 'Утро (6:00-12:00)'),
            ('afternoon', 'День (12:00-18:00)'),
            ('evening', 'Вечер (18:00-23:59)'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'morning':
            return queryset.filter(created_at__hour__gte=6, created_at__hour__lt=12)
        
        if self.value() == 'afternoon':
            return queryset.filter(created_at__hour__gte=12, created_at__hour__lt=18)
        
        if self.value() == 'evening':
            return queryset.filter(created_at__hour__gte=18)
        
        return queryset


class WordCountFilter(admin.SimpleListFilter):
    title = 'Количество слов'
    parameter_name = 'word_count'

    def lookups(self, request, model_admin):
        return (
            ('small', 'Короткие (до 10 слов)'),
            ('medium', 'Средние (10-30 слов)'),
            ('large', 'Длинные (более 30 слов)'),
        )
    
    def queryset(self, request, queryset):
        """
        На SQLite это не работает нормально.
        На PostgreSQL это работает нормально.
        """
        if self.value() == 'small':
            return queryset.filter(text__regex=r'^(\s*\S+){0,10}\s*$')
            
        if self.value() == 'medium':
            return queryset.filter(text__regex=r'^(\s*\S+){10,30}\s*$')
            
        if self.value() == 'large':
            return queryset.filter(text__regex=r'^(\s*\S+){30,}\s*$')
        
        return queryset


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    # list_display - те поля, которые будут отображаться в админке
    list_display = ('name', 'phone', 'created_at', 'status')
    # фильтры - на основе полей создаются автоматичски
    list_filter = (TimeOfDayFilter, 'status', 'created_at', 'master')
    # По каким полям можно искать
    search_fields = ('name', 'phone', 'comment')
    # Что будет кликабельным?
    list_display_links = ('name', 'phone')
    list_editable = ('status',)
    # Названия функций отвечающих за новые кнопки в админке
    actions = ['set_unconfirmed', 'set_confirmed', 'set_cancelled', 'set_completed']
    readonly_fields = ('created_at',)  # Показываем дату создания как нередактируемое поле
    filter_horizontal = ('services',)   # Делаем удобный виджет выбора услуг

    # Декоратор нам нужен чтобы кнопка называлась не как функция а на русском языке
    @admin.display(description='Изменить статус на "Не подтверждена"')
    def set_unconfirmed(self, request, queryset):
        queryset.update(status=0)

    @admin.display(description='Изменить статус на "Подтверждена"')
    def set_confirmed(self, request, queryset):
        queryset.update(status=1)

    @admin.display(description='Изменить статус на "Отменена"')
    def set_cancelled(self, request, queryset):
        queryset.update(status=2)
        
    @admin.display(description='Изменить статус на "Выполнена"')
    def set_completed(self, request, queryset):
        queryset.update(status=3)

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone')
    search_fields = ('first_name', 'last_name', 'phone')
    list_filter = ('services',)  # Фильтрация по услугам
    
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)
    search_fields = ('name', 'description')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # Определяем поля, которые будут отображаться в списке записей
    list_display = ('author_name', 'text', 'word_count', 'created_at', 'status', 'show_thumbnail')
    # Добавляем фильтры для удобной навигации по записям
    list_filter = (WordCountFilter, 'status', 'created_at')
    # Указываем поля, по которым можно производить поиск
    search_fields = ('author_name', 'text')
    # Поля, которые можно редактировать прямо в списке записей
    list_editable = ('status',)
    # Определение полей, которые нельзя редактировать
    readonly_fields = ('show_large_photo', 'created_at')
    # Настройка отображения полей в форме редактирования
    fieldsets = (
        (None, {
            'fields': ('author_name', 'text', 'photo', 'show_large_photo', 'status', 'created_at')
        }),
    )

    # Метод для подсчета количества слов в отзыве
    def word_count(self, obj):
        """Возвращает количество слов в отзыве."""
        return len(obj.text.split())
    word_count.short_description = 'Количество слов'

    # Метод для отображения миниатюры фотографии в списке записей
    @admin.display(description='Фото (миниатюра)')
    def show_thumbnail(self, obj):
        """Отображает миниатюру фото в списковом представлении."""
        if obj.photo:
            return format_html('<img src="{}" height="50" />', obj.photo.url)
        return "Нет фото"
    
    # Метод для отображения полноразмерной фотографии в детальном просмотре
    @admin.display(description='Фото (полный размер)')
    def show_large_photo(self, obj):
        """Отображает фото в детальном представлении."""
        if obj.photo:
            return format_html('<img src="{}"/>', obj.photo.url)
        return "Нет фото"
