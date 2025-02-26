from django.urls import path, include

from drfapp import views

urlpatterns = [
    
    path('index/', views.index),
    path('person/', views.person),
    path('user_login/', views.user_login),
    
    path("PersonAPI/", views.PersonAPI.as_view()),   #views.CLassName.as_view() 

]
