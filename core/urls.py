from django.urls import path
from . import views

urlpatterns = [
    # path('', views.ver_dias_creados),
    path('crear-dias/', views.crear_dias, name='crear_dias'),

    ##BOTONOES
    # path('next-day/<int:day_id>', views.next_day, name='next_day'),
    # path('back-day/<int:day_id>', views.back_day, name='back_day'),
    path('day/', views.ver_dia, name='today'),
    path('day/<int:day_id>', views.ver_dia, name='ver_dia'),
]