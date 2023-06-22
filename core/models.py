from django.db import models

# Create your models here.

class AccountBalance(models.Model):
    year = models.IntegerField(primary_key=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

class Day(models.Model):
    fecha = models.DateField(unique=True)
    # saldo_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    # Agrega otros atributos según tus necesidades

class Move(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    ingreso = models.BooleanField(default=False)
    egreso = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)


class History(models.Model):
    day = models.OneToOneField(Day, on_delete=models.CASCADE)
    move = models.ManyToManyField(Move, related_name='move' )