from audioop import reverse

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from movie.filters import MovieFilter, PersonFilter
from movie.models import Person, Movie, Genre
from movie.serializers import (
    PersonSerializer,
    MovieSerializer,
    GenreSerializer,
    MovieListSerializer,
    MovieDetailSerializer,
)
from movie.utils import CustomPagination


class ApiRoot(APIView):
    def get(self, request, format=None):
        return Response(
            {
                "people": reverse("person-list", request=request, format=format),
                "actors": reverse("person-list", request=request, format=None)
                + "?specialization=Actor",
                "directors": reverse("person-list", request=request, format=None)
                + "?specialization=Director",
                "movies": reverse("movie-list", request=request, format=format),
                "genres": reverse("genre-list", request=request, format=format),
            }
        )


class PersonListAPIView(APIView):
    filter = PersonFilter
    pagination_class = CustomPagination

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="specialization",
                type=str,
                description="Filter by specialization",
                required=False,
                location=OpenApiParameter.QUERY,
                enum=[option[0] for option in Person.SPECIALIZATION_CHOICES],
            ),
        ],
        responses={200: PersonSerializer(many=True)},
    )
    def get(self, request):
        people = self.filter(
            request.GET, queryset=Person.objects.all().order_by("id")
        ).qs
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(people, request)
        serializer = PersonSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        request=PersonSerializer,
        responses={200: PersonSerializer()},
    )
    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PersonDetailAPIView(APIView):
    @staticmethod
    def get_object(pk):
        return get_object_or_404(Person, pk=pk)

    @extend_schema(
        responses={200: PersonSerializer()},
    )
    def get(self, request, pk):
        person = self.get_object(pk)
        serializer = PersonSerializer(person)
        return Response(serializer.data)

    @extend_schema(
        request=PersonSerializer,
        responses={200: PersonSerializer()},
    )
    def put(self, request, pk):
        person = self.get_object(pk)
        serializer = PersonSerializer(person, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        person = self.get_object(pk)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieListAPIView(APIView):
    filter = MovieFilter
    pagination_class = CustomPagination

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="title",
                type=OpenApiTypes.STR,
                description="Filter by title",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="director",
                type=str,
                description="Filter by director name",
                required=False,
                location=OpenApiParameter.QUERY,
                enum=[
                    option
                    for option in Person.objects.filter(
                        specialization=Person.DIRECTOR
                    ).values_list("name", flat=True)
                ],
            ),
            OpenApiParameter(
                name="year",
                type=OpenApiTypes.INT,
                description="Filter by movie year",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="actor",
                type=str,
                description="Filter by actor name",
                required=False,
                location=OpenApiParameter.QUERY,
                enum=[
                    option
                    for option in Person.objects.filter(
                        specialization=Person.ACTOR
                    ).values_list("name", flat=True)
                ],
            ),
        ],
        responses={200: MovieSerializer(many=True)},
    )
    def get(self, request):
        movies = self.filter(
            request.GET,
            queryset=Movie.objects.select_related("director")
            .prefetch_related("genres", "actors")
            .order_by("id"),
        ).qs
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(movies, request)
        serializer = MovieListSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        request=MovieSerializer,
        responses={200: MovieDetailSerializer()},
    )
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MovieDetailAPIView(APIView):
    @staticmethod
    def get_object(pk):
        return get_object_or_404(Movie, pk=pk)

    @extend_schema(
        responses={200: MovieDetailSerializer()},
    )
    def get(self, request, pk):
        movie = self.get_object(pk)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)

    @extend_schema(
        request=MovieSerializer,
        responses={200: MovieDetailSerializer()},
    )
    def put(self, request, pk):
        movie = self.get_object(pk)
        serializer = MovieSerializer(movie, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        movie = self.get_object(pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreListAPIView(APIView):
    pagination_class = CustomPagination

    @extend_schema(
        responses={200: GenreSerializer(many=True)},
    )
    def get(self, request):
        genres = Genre.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(genres, request)
        serializer = GenreSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        request=GenreSerializer,
        responses={201: GenreSerializer()},
    )
    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GenreDetailAPIView(APIView):
    @staticmethod
    def get_object(pk):
        return get_object_or_404(Genre, pk=pk)

    @extend_schema(
        responses={200: GenreSerializer()},
    )
    def get(self, request, pk):
        genre = self.get_object(pk)
        serializer = GenreSerializer(genre)
        return Response(serializer.data)

    @extend_schema(
        request=GenreSerializer,
        responses={200: GenreSerializer()},
    )
    def put(self, request, pk):
        genre = self.get_object(pk)
        serializer = GenreSerializer(genre, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        genre = self.get_object(pk)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
