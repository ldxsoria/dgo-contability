from django.shortcuts import render, redirect

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

    ##################################
    ## SI NO EXISTE NINGUN DIA, LOS CREA #
    start = Day.objects.exists()
    if start  == True:
        pass
    else:
        crear = crear_dias(request)
    #################################


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


    saldo_ayer = Decimal(0)

    saldo_hoy = (saldo_ayer + suma_ingresos) + suma_egresos

    #LISTA HISTORIAL DEL DIA
    list_history = Move.objects.select_related('day_move').filter(day_move=dia_actual)


    #################################################
    ############# TEST CLASS
    historial = GenerarHistorico(dia_actual)
    print('#' * 20)
    print(historial.suma_ingresos)
    print(historial.suma_egresos)
    print(historial.saldo_hoy)
    print(historial.gen_history)
    print(f'Respueta automatica: {historial.saldo_ayer}')


    yesterday_id = int(dia_actual.id) - 1
    yesterday = Day.objects.get(id=yesterday_id)
    historial_yesterday = GenerarHistorico(yesterday)
    print(f'{yesterday}')
    print(historial_yesterday.saldo_hoy)
    
    #################################################
    ## FORMULARIO PARA AGREGAR MOVE (TRANSCACCION)

    #################################################

    context = {
        'today' : dia_actual,
        'next_day': int(dia_actual.id) + 1,
        'back_day': yesterday_id,
        'today_name': nombre,
        'egresos' : historial.suma_egresos,
        'ingresos': historial.suma_ingresos,
        'saldo_ayer' : historial.saldo_ayer,
        'saldo_hoy' : historial.saldo_hoy,
        'list_history': list_history
    }



    if request.method == 'GET':
        return render(request, 'app.html', context)
    else:
        if (request.POST['tipo'] == 'INGRESO'):
            valor_tipo = request.POST['valor']
        else:
            valor_negativo = request.POST['valor']
            valor_negativo = Decimal(valor_negativo) * -1
            print(valor_negativo)
            valor_tipo = Decimal(valor_negativo)

        new_move = Move(
            tipo = request.POST['tipo'],
            valor = valor_tipo,
            # realizado = request.POST[''],
            # comentario = request.POST[''],
            day_move = dia_actual
        )
        new_move.save()



        # return redirect(request, 'app.html', context)
        return redirect(request.path)



class GenerarSaldoAyer():
    def __init__(self, day):
        self.day = day

    def Get_saldo_ayer(self):

        pass


class GenerarHistorico():

    def __init__(self, day):
        self.day = day
        self.suma_ingresos = self.Gen_suma_ingresos()
        self.suma_egresos = self.Gen_suma_egresos()
        self.saldo_ayer = self.Get_saldo_ayer()
        self.saldo_hoy = self.Gen_saldo_hoy()
        self.gen_history = self.Gen_history()

    def Gen_history(self):
        history_exist = History.objects.filter(day=self.day).exists()

        if history_exist == True:
            history_update = History.objects.get(day=self.day)
            history_update.egresos_hoy = self.suma_egresos
            history_update.ingresos_hoy = self.suma_egresos
            history_update.saldo_hoy = self.saldo_hoy
            history_update.save()
            return 'Actualizado'

        else:
            new_history = History(day=self.day, egresos_hoy=self.suma_egresos, ingresos_hoy=self.suma_egresos, saldo_hoy=self.saldo_hoy)
            new_history.save()
            return 'Creado'  

    def Gen_saldo_hoy(self):
        total = self.suma_ingresos + self.suma_egresos + self.saldo_ayer
        return Decimal(total)


    def Get_saldo_ayer(self):
        day_anterior_id = int(self.day.id) - 1
        day_anterior = Day.objects.get(id=day_anterior_id)
        history_anterior_exist = History.objects.filter(day=day_anterior).exists()

        if history_anterior_exist:
            history_anterior = History.objects.get(day=day_anterior)
            saldo_ayer = history_anterior.saldo_hoy
        else:
            saldo_ayer = 0

        return Decimal(saldo_ayer)


    def Gen_suma_ingresos(self):
        ingresos = Move.objects.select_related('day_move').filter(day_move=self.day, tipo='INGRESO').values_list('valor')
        suma_ingresos = Decimal(0)
        for i in ingresos:
            suma_ingresos += i[0]
        
        return Decimal(suma_ingresos)

    
    def Gen_suma_egresos(self):
        egresos = Move.objects.select_related('day_move').filter(day_move=self.day, tipo='EGRESO').values_list('valor')
        suma_egresos = Decimal(0)
        for e in egresos:
            suma_egresos += e[0]
        
        return Decimal(suma_egresos)
    

    def __str__(self) :
        return f'{self.saldo_hoy}'
 

