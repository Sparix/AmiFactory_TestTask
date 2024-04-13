from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, Page
from django.db.models import QuerySet
from django.http import JsonResponse, Http404, HttpRequest
from django.views.generic import ListView, DetailView
from movies_api.models import Movie, Genre, Person


class GenreListView(ListView):
    model = Genre
    queryset = Genre.objects.all()

    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        data = list(self.get_queryset().values("id", "title"))
        return JsonResponse(data, safe=False)


class SerializeMovieMixin:
    def serialize_movie(self, movie: Movie) -> dict:
        return {
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "release_year": movie.release_year,
            "mpa_rating": movie.mpa_rating,
            "imdb_rating": float(movie.imdb_rating),
            "duration": movie.duration,
            "poster": movie.poster.url if movie.poster else "",
            "bg_picture": movie.bg_picture.url if movie.bg_picture else "",
            "genres": self.serialize_genres(movie.genres.all()),
            "directors": self.serialize_people(movie.directors.all()),
            "writers": self.serialize_people(movie.writers.all()),
            "stars": self.serialize_people(movie.stars.all()),
        }

    @staticmethod
    def serialize_genres(genres: QuerySet[Genre]) -> list[dict]:
        return [{"id": genre.id, "title": genre.title} for genre in genres]

    @staticmethod
    def serialize_people(people: QuerySet[Person]) -> list[dict]:
        return [
            {
                "id": person.id,
                "first_name": person.first_name,
                "last_name": person.last_name,
            }
            for person in people
        ]


class MovieListView(SerializeMovieMixin, ListView):
    model = Movie
    paginate_by = 5
    queryset = Movie.objects.prefetch_related(
        "genres", "directors", "writers", "stars"
    )

    def get(self, request: HttpRequest, *args, **kwargs):
        genre_id = self.request.GET.get("genre")
        src = self.request.GET.get("src")

        genre_error = self.validate_genre_id(genre_id)
        if genre_error:
            return JsonResponse({"error": genre_error}, status=400)

        src_error = self.validate_src(src)
        if src_error:
            return JsonResponse({"error": src_error}, status=400)

        queryset = self.get_queryset()
        if genre_id:
            queryset = queryset.filter(genres__id=int(genre_id))

        if src:
            queryset = queryset.filter(title__startswith=src)

        paginator = Paginator(queryset, self.paginate_by)

        page_number = self.request.GET.get("page", 1)
        try:
            page_obj = paginator.page(page_number)
        except EmptyPage:
            return JsonResponse({"errors": ["page__out_of_bounds"]})

        data = self.get_paginated_data(page_obj)
        return JsonResponse(data)

    @staticmethod
    def validate_genre_id(genre_id: id) -> None | str:
        if genre_id:
            try:
                int(genre_id)
            except ValueError:
                return "Invalid genre ID"

    @staticmethod
    def validate_src(src: str) -> None | str:
        if src:
            if not (2 <= len(src) <= 20):
                return "Invalid 'src' parameter length"

    def get_paginated_data(self, page_obj: Page) -> dict:
        serialized_movies = [self.serialize_movie(movie) for movie in page_obj]
        return {
            "total": page_obj.paginator.count,
            "pages": page_obj.paginator.num_pages,
            "results": serialized_movies,
        }


class MovieDetailView(SerializeMovieMixin, DetailView):
    model = Movie

    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        try:
            movie = self.get_object()
        except Http404:
            return JsonResponse({"error": ["movie_not_found"]}, status=404)
        serialized_movie = self.serialize_movie(movie)
        return JsonResponse(serialized_movie)
