from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse, Http404
from django.views.generic import ListView, DetailView
from movies_api.models import Movie, Genre


class GenreListView(ListView):
    model = Genre
    queryset = Genre.objects.all()

    def get(self, request, *args, **kwargs):
        data = list(self.get_queryset().values("id", "title"))
        return JsonResponse(data, safe=False)


class SerializeMovieMixin:
    def serialize_movie(self, movie):
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
    def serialize_genres(genres):
        return [{"id": genre.id, "title": genre.title} for genre in genres]

    @staticmethod
    def serialize_people(people):
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
    queryset = Movie.objects.all()

    def get_queryset(self):
        queryset = self.queryset

        genre_id = self.request.GET.get("genre")
        src = self.request.GET.get("src")
        if genre_id:
            try:
                queryset = queryset.filter(genres__id=int(genre_id))
            except ValueError:
                return JsonResponse({"error": ["genre__invalid"]}, status=400)

        if src:
            if len(src) < 2 or len(src) > 20:
                return JsonResponse({"error": ["src__invalid"]}, status=400)

            queryset = queryset.filter(title__startswith=src)

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page_number = self.request.GET.get("page", 1)
        paginator = Paginator(queryset, self.paginate_by)

        try:
            page_obj = paginator.page(page_number)
        except EmptyPage:
            return JsonResponse({"errors": ["page__out_of_bounds"]})

        data = self.get_paginated_data(page_obj)
        return JsonResponse(data)

    def get_paginated_data(self, page_obj):
        serialized_movies = [self.serialize_movie(movie) for movie in page_obj]
        return {
            "total": page_obj.paginator.count,
            "pages": page_obj.paginator.num_pages,
            "results": serialized_movies,
        }


class MovieDetailView(SerializeMovieMixin, DetailView):
    model = Movie

    def get(self, request, *args, **kwargs):
        try:
            movie = self.get_object()
        except Http404:
            return JsonResponse({"error": ["movie_not_found"]}, status=404)
        serialized_movie = self.serialize_movie(movie)
        return JsonResponse(serialized_movie)
