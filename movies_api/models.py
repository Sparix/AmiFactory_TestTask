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
