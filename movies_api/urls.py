from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from movies_api.views import GenreListView, MovieListView, MovieDetailView

urlpatterns = [
    path("genres/", GenreListView.as_view(), name="genres"),
    path("movies/", MovieListView.as_view(), name="movies"),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie_detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = "movies_api"
