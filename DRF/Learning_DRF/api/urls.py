from django.urls import path, include
from drfapp import views


from rest_framework.routers import DefaultRouter
from drfapp.views import PeopleViewSet

router = DefaultRouter()
router.register(r'people', PeopleViewSet, basename='people')
urlpatterns = router.urls

urlpatterns = [
    
    path('index/', views.index),
    path('person/', views.person),
    path('user_login/', views.user_login),
    
    path("PersonAPI/", views.PersonAPI.as_view()),   #views.CLassName.as_view() "<= OR =>" import the className directly then CLassName.as_view() will be the syntax !!

    path("",include(router.urls)),
    
    path("register/", views.RegisterAPI.as_view()),
    path("login/", views.LoginAPI.as_view()),
    
    path("paginator/", views.CustomPagination.as_view()),
    

]
