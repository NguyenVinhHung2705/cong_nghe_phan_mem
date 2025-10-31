from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # http://localhost:8000/dashboard/
]