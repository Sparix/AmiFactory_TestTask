from django.core.paginator import Paginator, EmptyPage, Page
from django.http import JsonResponse, Http404, HttpRequest
from django.views.generic import ListView, DetailView
from movies_api.models import Movie, Genre


class GenreListView(ListView):
    model = Genre
    queryset = Genre.objects.all()

    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        data = list(self.get_queryset().values("id", "title"))
        return JsonResponse(data, safe=False)


class MovieListView(ListView):
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
            return JsonResponse({"error": [genre_error]}, status=404)

        src_error = self.validate_src(src)
        if src_error:
            return JsonResponse({"error": [src_error]}, status=404)

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
            return JsonResponse({"errors": ["page__out_of_bounds"]}, status=404)

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

    @staticmethod
    def get_paginated_data(page_obj: Page) -> dict:
        serialized_movies = [movie.serialize() for movie in page_obj]
        return {
            "total": page_obj.paginator.count,
            "pages": page_obj.paginator.num_pages,
            "results": serialized_movies,
        }


class MovieDetailView(DetailView):
    model = Movie

    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        try:
            movie = self.get_object()
        except Http404:
            return JsonResponse({"error": ["movie_not_found"]}, status=404)
        return JsonResponse(movie.serialize())
