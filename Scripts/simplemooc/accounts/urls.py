from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

app_name = 'contas'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('entrar', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('sair', LogoutView.as_view(next_page='core:home'), name='logout'),
    path('cadastre-se', views.register, name='register'),
    path('nova-senha', views.password_reset, name='password_reset'),
    path('confirmar-nova-senha/<str:key>', views.password_reset_confirm, name='password_reset_confirm'),
    path('editar', views.edit, name='edit'),
    path('editar-senha', views.edit_password, name='edit_password')
]