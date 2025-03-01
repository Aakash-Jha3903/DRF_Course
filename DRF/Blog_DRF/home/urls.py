from django.urls import path

from . import views


urlpatterns = [
    path("blog/",views.BlogView.as_view()),
    path("all_blogs/",views.PublicBlogView.as_view()),
]
