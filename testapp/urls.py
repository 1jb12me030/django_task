# urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/place_order/', views.place_order, name='place_order'),
    path('api/place_order1/', views.place_order1, name='place_order'),
    path('api/add_address/', views.add_address, name='add_address'),
]
