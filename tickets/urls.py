
from django.urls import path
from . import views
from .views import MovieList


urlpatterns = [
  path("movies/",views.MovieList.as_view(),),
  path("movies/<int:pk>/",views.MovieDetils.as_view(),),
  #-------------------
  path("movies/", MovieList.as_view())
]
