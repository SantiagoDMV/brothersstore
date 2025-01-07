from django.contrib import admin
from .models import Finanzas
from .models import CategoriaGasto
from .models import Salarios

# Register your models here.
admin.site.register(Finanzas)
admin.site.register(CategoriaGasto)
admin.site.register(Salarios)