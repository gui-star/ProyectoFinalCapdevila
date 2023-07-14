from django.urls import path
from . import views

app_name = 'mensajes'

urlpatterns = [
    path('lista/', views.message_list, name='lista_mensajes'),
    path('enviar/', views.send_message, name='enviar_mensaje'),
    path('ver/<int:pk>/', views.view_message, name='ver_mensaje'),
    path('eliminar/<int:pk>/', views.delete_message, name='eliminar_mensaje'),

]
