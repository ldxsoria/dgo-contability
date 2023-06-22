from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from datetime import timedelta, date, datetime
from .models import Day, History, Move

from decimal import Decimal

def crear_dias(request):
    fecha_inicio = date(year=2023, month=1, day=1)
    fecha_fin = date(year=2023, month=12, day=31)
    
    delta = timedelta(days=1)
    fecha_actual = fecha_inicio
    
    while fecha_actual <= fecha_fin:
        Day.objects.create(fecha=fecha_actual)
        fecha_actual += delta
    
    return HttpResponse("Se han creado los objetos Dia para cada día del año.")

def nombre_del_dia(fecha):
    
    nombre_dia_semana = fecha.strftime('%A')

    if nombre_dia_semana == 'Monday':
        nombre_dia_semana = 'Lunes'
    elif nombre_dia_semana == 'Tuesday':
        nombre_dia_semana = 'Martes'    
    elif nombre_dia_semana == 'Wednesday':
        nombre_dia_semana = 'Miércoles'
    elif nombre_dia_semana == 'Thursday':
        nombre_dia_semana = 'Jueves'
    elif nombre_dia_semana == 'Friday':
        nombre_dia_semana = 'Viernes'
    elif nombre_dia_semana == 'Saturday':
        nombre_dia_semana = 'Sabado'
    elif nombre_dia_semana == 'Sunday':
        nombre_dia_semana = 'Domingo'
    else:
        nombre_del_dia = 'Error al convertir el dia, revisar VIEW'

    return f'{nombre_dia_semana}'


def ver_dia(request, day_id=None):
    fecha_actual = date.today()
    # Obtener el objeto Dia correspondiente a la fecha actual
    dia_actual = Day.objects.get(fecha=fecha_actual)
    # Obtener el ID del día actual


    if (day_id == None) or (day_id == dia_actual.id):
        nombre = nombre_del_dia(dia_actual.fecha)
        # return HttpResponse(f"El dia de hoy es: {nombre}")
    else:
        dia_actual = Day.objects.get(id=day_id)
        nombre = nombre_del_dia(dia_actual.fecha)
        # return HttpResponse(f"Es otro dia : {nombre}")

    # dia_actual = Day.objects.get(id=173)
    egresos = Move.objects.select_related('day_move').filter(day_move=dia_actual, tipo='EGRESO').values_list('valor')
    suma_egresos = 0
    for e in egresos:
        suma_egresos += e[0]


    ingresos = Move.objects.select_related('day_move').filter(day_move=dia_actual, tipo='INGRESO').values_list('valor')
    suma_ingresos = 0
    for e in ingresos:
        suma_ingresos += e[0]    


    saldo_ayer = Decimal(30)

    saldo_hoy = (saldo_ayer + suma_ingresos) + suma_egresos

    #LISTA HISTORIAL DEL DIA
    list_history = Move.objects.select_related('day_move').filter(day_move=dia_actual)

    context = {
        'today' : dia_actual,
        'next_day': int(dia_actual.id) + 1,
        'back_day': int(dia_actual.id) - 1,
        'today_name': nombre,
        'egresos' : suma_egresos,
        'ingresos': suma_ingresos,
        'saldo_ayer' : saldo_ayer,
        'saldo_hoy' : saldo_hoy,
        'list_history': list_history
    }

    return render(request, 'app.html', context)


class GenerarHistorico():
    dia_actual = Day.objects.get(id=173)


    def Gen_saldo_hoy(self):
        pass

    def Gen_suma_ingresos(self):
        pass

    
    def Gen_suma_egresos(self):
        egresos = Move.objects.select_related('day_move').filter(day_move=self.dia_actual, tipo='EGRESO').values_list('valor')
        suma_egresos = 0
        for e in egresos:
            suma_egresos += e[0]
        
        return suma_egresos
    


    #     new_ticket = Ticket(
    #     asunto=Asunto.objects.get(id=request.POST['asunto']),
    #     descripcion=request.POST['descripcion'],
    #     solicitante=request.user,
    #     )
    # new_ticket.save()


    pass 

