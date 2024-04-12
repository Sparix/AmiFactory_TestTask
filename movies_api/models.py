from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Genre(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title


class Person(models.Model):
    class TypeChoices(models.TextChoices):
        DIRECTOR = "DR", "Director"
        WRITER = "WR", "Writer"
        ACTOR = "AC", "Actor"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    types = models.CharField(max_length=2, choices=TypeChoices.choices)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    class MpaRatingChoices(models.TextChoices):
        G_RATING = "G", "G"
        PG_RATING = "PG", "PG"
        PG13_RATING = "PG13", "PG13"
        R_RATING = "R", "R"
        NC17_RATING = "NC17", "NC17"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=5000, blank=True)
    poster = models.ImageField(upload_to="images/poster/", null=True)
    bg_picture = models.ImageField(upload_to="images/bg_picture/", null=True)
    release_year = models.IntegerField()
    mpa_rating = models.CharField(max_length=5, choices=MpaRatingChoices.choices)
    imdb_rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
    )
    duration = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name="genres_movie")
    directors = models.ManyToManyField(Person, related_name="directors_movie")
    writers = models.ManyToManyField(Person, related_name="writers_movie")
    stars = models.ManyToManyField(Person, related_name="stars_movie")

    def __str__(self) -> str:
        return (
            f"name: {self.title}"
            f"imdb_rating: {self.imdb_rating}"
            f"duration: {self.duration}"
        )
