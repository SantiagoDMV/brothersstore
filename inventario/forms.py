from .models import Producto, Categoria
from django.forms import ModelForm

class crear_producto(ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'cantidad', 'categoria', 'precio', 'imagen_url']
        
class crear_categoria(ModelForm):
    class Meta:
        model= Categoria
        fields = ['nombre', 'descripcion']
    