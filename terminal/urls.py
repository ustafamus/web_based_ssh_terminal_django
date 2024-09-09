from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('terminal/', views.terminal_view, name='terminal'),
    path('connect/', views.connect_ssh, name='connect_ssh'),
    path('execute_command/', views.execute_command, name='execute_command'),


]
