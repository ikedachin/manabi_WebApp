from django.urls import path
from . import views

urlpatterns = [
    path('indes', views.HogehogeClass.as_view())
]
