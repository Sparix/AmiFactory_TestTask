from django.urls import path

from movies_api.views import GenreListView

urlpatterns = [
    path("genres/", GenreListView.as_view(), name="genres"),
]

app_name = "movies_api"
