from django.urls import path
from . import views

urlpatterns = [
    
    path('producto/',views.lista_producto, name = "lista_producto")
]