import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Person, Movie, Genre
from .views import PersonListAPIView, MovieListAPIView


class PersonListAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.view = PersonListAPIView.as_view()

    def test_get_persons(self):
        actor = Person.objects.create(name="Alice", specialization=Person.ACTOR)
        director = Person.objects.create(name="Bob", specialization=Person.DIRECTOR)

        url = reverse('person-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_get_only_actors(self):
        actor = Person.objects.create(name="Alice", specialization=Person.ACTOR)
        director = Person.objects.create(name="Bob", specialization=Person.DIRECTOR)

        url = reverse('person-list')
        response = self.client.get(url, {'specialization': Person.ACTOR})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], actor.name)

    def test_create_person(self):
        new_person_data = {
            "name": "Charlie Brown",
            "specialization": Person.ACTOR
        }

        url = reverse('person-list')
        response = self.client.post(url, data=new_person_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Person.objects.filter(name="Charlie Brown").exists())


class MovieListAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.view = MovieListAPIView.as_view()

    def test_get_movies(self):
        actor = Person.objects.create(name="John Doe", specialization=Person.ACTOR)
        director = Person.objects.create(name="Jane Smith", specialization=Person.DIRECTOR)

        movie1 = Movie.objects.create(title="Movie 1", description="Description 1", duration=120, year=2022,
                                      director=director)
        movie1.actors.add(actor)

        movie2 = Movie.objects.create(title="Movie 2", description="Description 2", duration=150, year=2022,
                                      director=director)
        movie2.actors.add(actor)

        url = reverse('movie-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_create_movie(self):
        actor = Person.objects.create(name="John Doe", specialization=Person.ACTOR)
        director = Person.objects.create(name="Jane Smith", specialization=Person.DIRECTOR)

        new_movie_data = {
            "title": "New Movie",
            "description": "New Description",
            "duration": 130,
            "year": 2023,
            "director": director.id,
            "actors_ids": [actor.id]
        }

        url = reverse('movie-list')
        response = self.client.post(url, data=new_movie_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Movie.objects.filter(title="New Movie").exists())


class MovieDetailAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.movie = Movie.objects.create(title="Movie 1", description="Description 1", duration=120, year=2022)

    def test_get_movie(self):
        url = reverse('movie-detail', kwargs={'pk': self.movie.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.movie.title)

    def test_update_movie(self):
        url = reverse('movie-detail', kwargs={'pk': self.movie.pk})

        updated_data = {"title": "Updated Movie", "description": "Updated Description", "duration": 150, "year": 2023}
        response = self.client.put(url, data=updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, updated_data["title"])
        self.assertEqual(self.movie.description, updated_data["description"])
        self.assertEqual(self.movie.duration, updated_data["duration"])
        self.assertEqual(self.movie.year, updated_data["year"])

    def test_delete_movie(self):
        url = reverse('movie-detail', kwargs={'pk': self.movie.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Movie.objects.filter(pk=self.movie.pk).exists())


class MovieFilterTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.actor = Person.objects.create(name="John Doe", specialization=Person.ACTOR)
        self.director = Person.objects.create(name="Jane Smith", specialization=Person.DIRECTOR)

        self.movie1 = Movie.objects.create(title="Movie 1", description="Description 1", duration=120, year=2022,
                                           director=self.director)
        self.movie2 = Movie.objects.create(title="Movie 2", description="Description 2", duration=150, year=2022,
                                           director=self.director)
        self.movie1.actors.add(self.actor)

    def test_actor_filter(self):
        url = reverse('movie-list')
        response = self.client.get(url, {'actor': self.actor.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(len(response.data['results']), 1)

    def test_director_filter(self):
        url = reverse('movie-list')
        response = self.client.get(url, {'director': self.director.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_title_filter(self):
        url = reverse('movie-list')
        response = self.client.get(url, {'title': 'Movie 1'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class GenreListAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.genre_data = {'name': 'Drama'}
        self.invalid_genre_data = {'name': ''}

    def test_create_genre(self):
        url = reverse('genre-list')
        response = self.client.post(url, self.genre_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Genre.objects.count(), 1)
        self.assertEqual(Genre.objects.get().name, 'Drama')

    def test_create_invalid_genre(self):
        url = reverse('genre-list')
        response = self.client.post(url, self.invalid_genre_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GenreDetailAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.genre = Genre.objects.create(name='Comedy')

    def test_get_genre(self):
        url = reverse('genre-detail', kwargs={'pk': self.genre.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Comedy')

    def test_update_genre(self):
        url = reverse('genre-detail', kwargs={'pk': self.genre.pk})
        updated_data = {'name': 'Action'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Genre.objects.get(pk=self.genre.pk).name, 'Action')

    def test_delete_genre(self):
        url = reverse('genre-detail', kwargs={'pk': self.genre.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Genre.objects.count(), 0)
