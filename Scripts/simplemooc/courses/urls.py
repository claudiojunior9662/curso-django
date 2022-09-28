from django.urls import path

from . import views

app_name = 'cursos'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>', views.details, name='details'),
]