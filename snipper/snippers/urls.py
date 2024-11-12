from django.urls import path
from . import views

urlpatterns = [
    path('snippers/', views.snippers, name='snippers'),
]
