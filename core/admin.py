from django.contrib import admin

# Register your models here.
from .models import Day, AccountBalance, Move, History

admin.site.register(Day)
admin.site.register(AccountBalance)
admin.site.register(Move)
admin.site.register(History)
