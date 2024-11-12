from django.urls import path
from .views import LoginView, LogoutView, ProfileView

app_name = 'users' # Имя для пространства имён
"""
Теперь к урлам этого приложения мы будем обращаться как users:login
"""

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]