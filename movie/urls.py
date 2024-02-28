from django.urls import path
from movie.views import (
    PersonListAPIView,
    PersonDetailAPIView,
    MovieListAPIView,
    MovieDetailAPIView,
    GenreListAPIView,
    GenreDetailAPIView,
)

urlpatterns = [
    path("people/", PersonListAPIView.as_view(), name="person-list"),
    path("people/<int:pk>/", PersonDetailAPIView.as_view(), name="person-detail"),
    path("movies/", MovieListAPIView.as_view(), name="movie-list"),
    path("movies/<int:pk>/", MovieDetailAPIView.as_view(), name="movie-detail"),
    path("genres/", GenreListAPIView.as_view(), name="genre-list"),
    path("genres/<int:pk>/", GenreDetailAPIView.as_view(), name="genre-detail"),
]
