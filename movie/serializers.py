from rest_framework import serializers

from movie.models import (
    Genre,
    Person,
    Movie,
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("id", "name", "specialization")


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "description",
            "duration",
            "genres",
            "actors",
            "year",
            "director",
        )

    @staticmethod
    def validate_actors(actors):
        for actor in actors:
            if actor.specialization != Person.ACTOR:
                raise serializers.ValidationError(f"No actor with {actor.pk} pk")
        return actors

    @staticmethod
    def validate_director(director):
        if director.specialization != Person.DIRECTOR:
            raise serializers.ValidationError(f"No director with {director.pk} pk")
        return director


class MovieListSerializer(MovieSerializer):
    genres = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    actors = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    director = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Movie
        fields = ("id", "title", "genres", "actors", "image", "director")


class MovieDetailSerializer(MovieSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = PersonSerializer(many=True, read_only=True)
    director = PersonSerializer(many=False, read_only=True)

    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "duration",
            "description",
            "genres",
            "actors",
            "image",
            "director",
        )


class MovieImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("id", "image")
