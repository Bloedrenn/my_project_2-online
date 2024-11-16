from django.contrib import admin
from .models import Visit, Master, Service, Review


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


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    # list_display - те поля, которые будут отображаться в админке
    list_display = ('name', 'phone', 'created_at', 'status')
    # фильтры - на основе полей создаются автоматичски
    list_filter = (TimeOfDayFilter, 'status', 'created_at', 'master')
    search_fields = ('name', 'phone', 'comment')

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
    list_display = ('author_name', 'created_at', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('author_name', 'text')
    list_editable = ('status',)
