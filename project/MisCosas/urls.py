from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('css', views.css,name='css'),
    path('register/', views.register, name='register'),
    path('logout/',views.logout_view, name='logout'),
    path('user/<str:llave>',views.user, name='user'),
    path('users/',views.users, name='users'),
    path('login/',views.login_view, name='login'),
    path('informacion/',views.informacion, name='informacion'),
    path('<str:llave1>/<str:llave2>', views.processalimentador, name= 'processalimentador'),
    path('<str:llave>/<str:llave1>/<str:llave2>/De-Seleccionar', views.borrarprincipal, name= 'borrarprincipal'),
    path('<str:llave>/<str:llave1>/<str:llave2>', views.processitem, name= 'processitem'),
    path('alimentadores/', views.alimentadores, name='alimentadores'),
    path('<str:llave>/<str:llave1>/<str:llave2>/<str:llave3>/votopositivo/', views.gestionvotos, name='gestionvotos'),
    path('<str:llave>/<str:llave1>/<str:llave2>/<str:llave3>/votonegativo/', views.gestionvotos, name='gestionvotos'),
]