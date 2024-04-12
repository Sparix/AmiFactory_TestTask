from django.urls import path

from movies_api.views import GenreListView, MovieListView, MovieDetailView

urlpatterns = [
    path("genres/", GenreListView.as_view(), name="genres"),
    path("movies/", MovieListView.as_view(), name="movies"),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie_detail")
]

app_name = "movies_api"
