from django.urls import path, include

from drfapp import views

urlpatterns = [
    
    path('index/', views.index),
    path('person/', views.person)

]
