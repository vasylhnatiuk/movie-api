from django.contrib import admin

from .models import Genre, Movie, Person

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Person)
