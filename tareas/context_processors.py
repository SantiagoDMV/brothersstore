from django.contrib.auth.models import Group
from ventas.models import Venta

def grupos_usuario(request):
    if request.user.is_authenticated:
        try:
            grupo = request.user.groups.all()[0]  # Obtén todos los grupos del usuario
            return {'grupos': grupo}
        except:
            return {'grupo': 'adminitracion'}
    return {'grupo': []}  # Devuelve una lista vacía si no hay usuario logueado


def total_ventas(request):
    try:
        ventas_realizadas = Venta.objects.all()
        suma_ventas = sum(float(venta.total) for venta in ventas_realizadas)  # Sumamos las ventas totales
        #suma_ventas = (26.6 + 175.73 + 69.90 + 30) - 26.46
    # El negocio se queda con el 60%
        pago_negocio = round(suma_ventas * 0.6, 2)

    # El restante es el 40% para los empleados
        restante_para_empleados = suma_ventas - pago_negocio

    # Dividimos el restante entre los empleados
        pago_santiago = round(restante_para_empleados * 0.6, 2)
        pago_raul = round(restante_para_empleados * 0.2, 2)
        pago_andrea = round(restante_para_empleados * 0.2, 2)

        return {
            'total_ventas': suma_ventas,
            'pago_negocio': pago_negocio,
            'restante_empleados': restante_para_empleados,
            'pago_santiago': pago_santiago,
            'pago_raul': pago_raul,
            'pago_andrea': pago_andrea,
        }
    except:
        return {
            'total_ventas': 0,
            'pago_negocio': 0,
            'restante_empleados': 0,
            'pago_santiago': 0,
            'pago_raul': 0,
            'pago_andrea': 0,
        }
