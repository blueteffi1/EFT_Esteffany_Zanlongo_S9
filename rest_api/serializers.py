from rest_framework import serializers
from misite.models import Categoria, Producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id_producto','nombre', 'categoria', 'precio']


class Categoria(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id_categoria','nombre']



    