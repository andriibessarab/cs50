from django.urls import path

from . import views

urlpatterns = [
    path('', views.main),
    path('history', views.history),

    path('register', views.register),
    path('logIn', views.logIn),
    path('logOut', views.logOut),

    path('track', views.track),
    path("createNewCategory", views.addNewCategory),

    path('requestInformation', views.requestInformation),
]