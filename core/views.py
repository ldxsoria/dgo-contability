from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from datetime import timedelta, date, datetime
from .models import Day, History

def crear_dias(request):
    fecha_inicio = date(year=2023, month=1, day=1)
    fecha_fin = date(year=2023, month=12, day=31)
    
    delta = timedelta(days=1)
    fecha_actual = fecha_inicio
    
    while fecha_actual <= fecha_fin:
        Day.objects.create(fecha=fecha_actual)
        fecha_actual += delta
    
    return HttpResponse("Se han creado los objetos Dia para cada día del año.")

def ver_dias_creados(request):
    fecha_actual = date.today()
    # Obtener el objeto Dia correspondiente a la fecha actual
    dia_actual = Day.objects.get(fecha=fecha_actual)
    # Obtener el ID del día actual

    now = datetime.now()
    nombre_dia_semana = now.strftime('%A')

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


    #LISTA HISTORIAL DEL DIA
    list_history = History.objects.select_related('day')
    context = {
        'today' : dia_actual,
        'today_name': nombre_dia_semana,
        'list_history': list_history
    }

    return render(request, 'app.html', context)

def next_day(request, day_id):
    day_id = day_id + 1

    dia_actual = Day.objects.get(id = day_id)
    # Obtener el ID del día actual

    now = dia_actual.fecha
    nombre_dia_semana = now.strftime('%A')

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

    context = {
        'today' : dia_actual,
        'today_name': nombre_dia_semana
    }

    return render(request, 'app.html', context)

def back_day(request, day_id):
    day_id = day_id - 1
    dia_actual = Day.objects.get(id = day_id)
    # Obtener el ID del día actual

    now = dia_actual.fecha
    nombre_dia_semana = now.strftime('%A')

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

    context = {
        'today' : dia_actual,
        'today_name': nombre_dia_semana
    }

    return render(request, 'app.html', context)

