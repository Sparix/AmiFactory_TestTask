from django.contrib import admin

from movies_api.models import Genre, Person, Movie


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_filter = ("title",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ("last_name", "types")
    list_filter = ("types",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "release_year",
        "mpa_rating",
        "imdb_rating",
        "duration",
        "created_at",
    )
    list_filter = ("imdb_rating", "mpa_rating",)
