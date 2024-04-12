from django.urls import path

from movies_api.views import GenreListView, MovieListView

urlpatterns = [
    path("genres/", GenreListView.as_view(), name="genres"),
    path("movies/", MovieListView.as_view(), name="movies")
]

app_name = "movies_api"
