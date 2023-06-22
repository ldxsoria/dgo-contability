from django.db import models

# Create your models here.

class AccountBalance(models.Model):
    year = models.IntegerField(primary_key=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)


class Day(models.Model):
    fecha = models.DateField(unique=True)
    #UN DIA TIENE UN HISTORIAL

    def __str__(self) :
        return f'{self.id} ({self.fecha})'
    
class Move(models.Model):
    class MoveType(models.TextChoices):
        INGRESO = 'INGRESO', 'INGRESO'
        EGRESO = 'EGRESO', 'EGRESO'

    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(
        max_length=7,
        choices=MoveType.choices,
        default=MoveType.EGRESO
    )

    realizado = models.BooleanField(default=False)


    created_at = models.DateField(auto_now_add=True)
    #FK
    day_move = models.ForeignKey(Day, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.tipo} - {self.day_move} : S/ {self.valor}'

class History(models.Model):
    move = models.ManyToManyField(Move, blank=True)
    saldo_ayer = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gastos_hoy = models.DecimalField(max_digits=10, decimal_places=2,  null=True, blank=True)
    saldo_hoy = models.DecimalField(max_digits=10, decimal_places=2,  null=True, blank=True)