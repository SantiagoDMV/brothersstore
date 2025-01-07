from django import forms
from .models import Finanzas, Salarios

class crear_finanza(forms.ModelForm):
    class Meta:
        model= Finanzas
        fields = ['usuario','categoria_gasto','descripcion', 'monto', 'metodo_pago', 'comprobante_url']
        
class crear_salario(forms.ModelForm):
    class Meta:
        model = Salarios
        fields = ['usuario', 'monto', 'estado']
    