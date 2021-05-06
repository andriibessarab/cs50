from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="main"),
    path("registerProcess", views.registerProcess, name="registerProcess"),
    path("loginProcess", views.loginProcess, name="loginProcess"),
    path("logoutProcess", views.logoutProcess, name="logoutProcess"),
    path("placeOrder", views.placeOrder, name="placeOrder"),
]