from django.http import JsonResponse
from django.views.generic import ListView
from movies_api.models import Genre


class GenreListView(ListView):
    model = Genre
    queryset = Genre.objects.all()

    def get(self, request, *args, **kwargs):
        data = list(self.get_queryset().values("id", "title"))
        return JsonResponse(data, safe=False)
