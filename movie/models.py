from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Person(models.Model):
    ACTOR = "Actor"
    DIRECTOR = "Director"

    SPECIALIZATION_CHOICES = [
        (ACTOR, "Actor"),
        (DIRECTOR, "Director"),
    ]

    name = models.CharField(max_length=255)
    specialization = models.CharField(
        max_length=255, choices=SPECIALIZATION_CHOICES, default=ACTOR
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "People"


class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    duration = models.IntegerField(null=True)
    genres = models.ManyToManyField(Genre, blank=True)
    actors = models.ManyToManyField(Person, blank=True, related_name="actors_movies")
    director = models.ForeignKey(
        Person, blank=True, null=True, on_delete=models.SET_NULL, related_name="movies"
    )
    year = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
