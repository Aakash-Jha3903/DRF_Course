from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    # path('admin/', admin.site.urls),
    path("register/",views.RegisterView.as_view()),
    path("login/",views.LoginView.as_view()),
]
