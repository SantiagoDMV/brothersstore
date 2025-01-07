from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from ventas.models import Venta, MetodoPago, EstadoVenta
from .forms import crear_finanza, crear_salario
from .models import Finanzas, CategoriaGasto, Salarios
from ventas.models import TotalVentas
from ventas.forms import crear_total_ventas

# Create your views here.
def registro(request):
    if(request.method == 'GET'):
        return render(request, 'registro.html', {  
            "form" : UserCreationForm
        })
    else: 
        try:
            if(request.POST['password1'] == request.POST['password2']):
                print(request.POST)
                usuario = User.objects.create_user(username=request.POST['username'], password=request.POST["password1"])
                usuario.save()
                login(request,usuario)
                return redirect('home')
        except IntegrityError:
            if request.method == 'POST':
                return render(request, 'registro.html', {  
                'error' : 'El usuario ya existe',
                "form" : UserCreationForm
            })
        return render(request, 'registro.html', {  
                'error' : 'Ingrese datos validos',
                "form" : UserCreationForm
            })
def login_usuario(request):
    if request.method == 'POST':
        try:
            user = authenticate(request, username= request.POST['username'], password = request.POST['password'])
            if user is None:
                return render(request, 'login.html',{
                    "form": AuthenticationForm,
                    'error': 'El usuario no existe'
                })  
            else:   
                login(request,user)
                return redirect('home')
        except ValueError:
            return render(request, 'login.html',{
                "form": AuthenticationForm,
                'error': 'Ingrese datos válidos'
            })
    else:
        if request.method == 'GET':
            return render(request, 'login.html',{
                "form": AuthenticationForm
            })
            
@login_required
def logout_usuario(request):
    logout(request)
    return redirect('home')
        
def home(request):
    if request.method == 'GET':
        salarios_trabajadores = Salarios.objects.all()
        try:
            ventas_realizadas = Venta.objects.all()
            gastos_realizados = Finanzas.objects.all()
            estado_pagado = get_object_or_404(EstadoVenta, nombre = 'Pagado')
            
            salarios_realizados = Salarios.objects.filter(estado = estado_pagado.id)
            
            suma = TotalVentas.objects.order_by('-creado_en').first()
            if(suma):
                suma = float(suma.total)
            else: 
                suma = 0
            
            suma_gastos = 0
            suma_salarios = 0
            
            for salario in salarios_realizados:
                suma_salarios = suma_salarios + salario.monto
            for gasto in gastos_realizados:
                suma_gastos = suma_gastos + gasto.monto
            
        #if ventas_realizadas
            return render(request, 'home.html',{
                'total_ventas' : suma - float(suma_gastos),
                'ventas' : ventas_realizadas,
                'salarios_trabajadores' : salarios_trabajadores 
            })
        except ValueError:
            print(ValueError)
            return render(request, 'home.html',{
                'total_ventas' : [],
                'ventas' : [],
                'salarios_trabajadores' : []
            })
        
def page_gastos(request):
    try:
        gastos_obtenidos = Finanzas.objects.all()
        return render(request, 'gastos.html',{
        'gastos': gastos_obtenidos
        })
    except:
        gastos_obtenidos = Finanzas.objects.all()
        return render(request, 'gastos.html',{
        'gastos': []
        })
    
def page_mercaderia(request):
    return render(request, 'mercaderia.html',{  
    })
    
    
def vista_salarios(request):
    if request.method == 'GET':
        try:
            salarios_instancias = Salarios.objects.all()
            return render(request, 'vista-salarios.html', {
            'salarios': salarios_instancias
            })
        except:
            return render(request, 'vista-salarios.html', {
            'salarios': []
            })
    else:
        if request.method == 'POST':
            try:
                usuario_instancia = get_object_or_404(User, pk= int(request.POST['categoria_gasto']))
                metodo_instancia = get_object_or_404(MetodoPago, pk = int(request.POST['metodo_pago']))
                nuevo_pago_salario = Finanzas.objects.create(
                    usuario = usuario_instancia,
                    monto = float(request.POST['monto']),
                ) 
                
                return redirect('gastos')
                
            except:
                return render(request, 'pago_salario.html', {
                    'form': crear_finanza  
                })
    
def crear_pago_salario(request, salario_id):
    if request.method == 'GET':
        try:
            salario_instancia = get_object_or_404(Salarios, pk = salario_id)
            form = crear_salario(instance=salario_instancia)
            return render(request, 'salarios.html', {
            'salario': salario_instancia,
            'form': form
            })
        except:
            return render(request, 'salarios.html', {
            'form': [],
            'salario': []
            })
    else:
        if request.method == 'POST':
            try:
                
                instancia = get_object_or_404(Salarios, pk = salario_id)
                diferencia = float(instancia.monto) - float(request.POST['monto'])
                if diferencia == 0:
                    instancia_estado = get_object_or_404(EstadoVenta, nombre = 'Pagado')
                else:
                    instancia_estado = get_object_or_404(EstadoVenta, nombre = 'Pendiente')
                    
                instancia_total_ventas = TotalVentas.objects.latest('creado_en')
                actualizar_total_ventas =crear_total_ventas(
                    {
                      'total': round(float(instancia_total_ventas.total) - float(request.POST['monto']), 2),
                    },
                    instance=instancia_total_ventas
                )
                print(actualizar_total_ventas)
                
                if hasattr(actualizar_total_ventas, 'is_valid') and actualizar_total_ventas.is_valid():
                    actualizar_total_ventas.save()
                    print('Actualización realizada correctamente')
                else:
                    print('Errores al actualizar:', getattr(actualizar_total_ventas, 'errors', 'Error desconocido'))
                
                actualizacion_salario = crear_salario(
                    {
                        'usuario' : get_object_or_404(User, pk = instancia.usuario.id),
                        'monto': round(diferencia,2),
                        'estado' :instancia_estado
                    }
                    , instance=instancia)
                if hasattr(actualizacion_salario, 'is_valid') and actualizacion_salario.is_valid():
                    actualizacion_salario.save()
                    print('Actualización realizada correctamente')
                else:
                    print('Errores al actualizar:', getattr(actualizacion_salario, 'errors', 'Error desconocido'))

                return redirect('vista-salarios')
            except ValueError:
                print(ValueError)
                return redirect('vista-salarios')
        
def actualizar_pago_salario(request,pago_salario_id):
    if request.method == 'GET':
        instancia_pago_salario = get_object_or_404(Finanzas, pk = pago_salario_id)
        form_instancia_pago = crear_finanza(instance=instancia_pago_salario)
        return render(request, 'actualizar-pago-salario.html',{
            'form': form_instancia_pago,
            'instancia': instancia_pago_salario
        })
    else:
        if request.method == 'POST':
            instancia_pago_salario = get_object_or_404(Finanzas, pk = pago_salario_id)
            form_instancia_pago = crear_finanza(request.POST, instance=instancia_pago_salario)
            form_instancia_pago.save()
            return redirect('gastos')
    
def eliminar_pago_salario(request,pago_salario_id):
    if request.method == 'POST':
        instancia_pago_salario = get_object_or_404(Finanzas, pk = pago_salario_id)
        instancia_pago_salario.delete()
        return redirect('gastos')

def calcular_salarios(request):
    try:
        ventas_realizadas = Venta.objects.all()
        suma_ventas = sum(float(venta.total) for venta in ventas_realizadas)  # Sumamos las ventas totales
        
        TotalVentas.objects.create(
            total = suma_ventas,
            user = request.user
        )
        
        pago_negocio = round(suma_ventas * 0.6, 2)

    # El restante es el 40% para los empleados
        restante_para_empleados = suma_ventas - pago_negocio

    # Dividimos el restante entre los empleados
        pago_santiago = round(restante_para_empleados * 0.6, 2)
        pago_raul = round(restante_para_empleados * 0.2, 2)
        pago_andrea = round(restante_para_empleados * 0.2, 2)
        
        usuarios = User.objects.all()
        estado_instancia =get_object_or_404(EstadoVenta, nombre = 'Pendiente')
        for usuario in usuarios:
            print(usuario.username)
            if usuario.username == 'santy':
                Salarios.objects.create(
                    usuario = get_object_or_404(User, pk = usuario.id),
                    monto = float(pago_santiago),
                    estado =estado_instancia
                )
            if usuario.username == 'Brothers_Store_Riobamba':
                Salarios.objects.create(
                    usuario = get_object_or_404(User, pk = usuario.id),
                    monto = float(pago_negocio),
                    estado =estado_instancia
                )
            if usuario.username == 'raul':
                Salarios.objects.create(
                    usuario = get_object_or_404(User, pk = usuario.id),
                    monto = float(pago_raul),
                    estado =estado_instancia
                )
            if usuario.username == 'andrea':
                Salarios.objects.create(
                    usuario = get_object_or_404(User, pk = usuario.id),
                    monto = float(pago_andrea),
                    estado = estado_instancia
                )
            
        return redirect('home')    
    except ValueError:
        print(ValueError)
        return render(request, 'salarios.html',{
        'total': []
    })
    
    
    #salario_brothersStore = 