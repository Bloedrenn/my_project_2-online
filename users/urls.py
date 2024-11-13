from django.urls import path
from . import views

app_name = 'cabinet' # Имя для пространства имён
"""
Теперь к урлам этого приложения мы будем обращаться как cabinet:название_маршрута
"""

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('all-visits/', views.ProfileVisitsListView.as_view(), name='all_visits'),
    path('new-visits/', views.ProfileVisitsListView.as_view(), {'visit_type': 'new'}, name='new_visits'),
    path('visit-archive/', views.ProfileVisitsListView.as_view(), {'visit_type': 'archive'}, name='visit_archive'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('visit/<int:pk>/', views.VisitDetailView.as_view(), name='visit_detail'),
    path('visit/<int:pk>/delete/', views.VisitDeleteView.as_view(), name='visit_delete'),
    path('visit/<int:pk>/update/', views.VisitUpdateView.as_view(), name='visit_update'),
]