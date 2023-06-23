from django.urls import path
from . import views

urlpatterns = [
    # path('', views.ver_dias_creados),
    path('crear-dias/', views.crear_dias, name='crear_dias'),

    #BOTONOES
    path('', views.ver_dia, name='index'),
    path('day/', views.ver_dia, name='today'),
    path('day/<int:day_id>', views.ver_dia, name='ver_dia'),
]