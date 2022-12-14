from django.urls import path

from . import views

app_name = 'cursos'
urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>', views.details, name='details'),
    path('<slug:slug>/inscricao/', views.enrollment, name='enrollment'),
    path('<slug:slug>/cancelar-inscricao/', views.undo_enrollment, name='undo_enrollment'),
    path('<slug:slug>/anuncios/', views.announcements, name='announcements'),
    path('<slug:slug>/anuncios/<int:pk>/', views.show_announcement, name='show_announcement'),
]