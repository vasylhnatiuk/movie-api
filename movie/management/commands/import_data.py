import json
import requests
from django.core.management.base import BaseCommand
from movie.models import Movie, Genre, Person

MOVIE_TITLES = [
    "The Shawshank Redemption",
    "The Godfather",
    "The Dark Knight",
    "Pulp Fiction",
    "Forrest Gump",
    "Schindler's List",
    "The Lord of the Rings: The Return of the King",
    "Fight Club",
    "The Matrix",
    "Inception",
    "The Silence of the Lambs",
    "The Green Mile",
    "The Godfather: Part II",
    "The Lord of the Rings: The Fellowship of the Ring",
    "Goodfellas",
    "The Lord of the Rings: The Two Towers",
    "The Usual Suspects",
    "Se7en",
    "The Pianist",
    "Gladiator",
    "The Departed",
    "Saving Private Ryan",
    "The Prestige",
    "The Lion King",
    "American History X",
    "Braveheart",
    "The Shining",
    "The Intouchables",
    "The Terminator",
    "The Sixth Sense",
    "Interstellar",
    "Back to the Future",
    "Django Unchained",
    "The Avengers",
    "The Dark Knight Rises",
    "Inglourious Basterds",
    "The Matrix Reloaded",
    "The Matrix Revolutions",
    "Star Wars: Episode IV - A New Hope",
    "Star Wars: Episode V - The Empire Strikes Back"
]

OMDB_API_KEY = "f62367fe"


class Command(BaseCommand):
    help = 'Populate database with data from OMDB API'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t="

    def handle(self, *args, **options):
        for title in MOVIE_TITLES:
            try:
                api_url = self.build_api_url(title)
                data = self.fetch_data(api_url)
                print(data)
                movie_data = self.extract_movie_data(data)
                self.create_movie(movie_data)
                self.stdout.write(self.style.SUCCESS(f'"{title}" imported successfully'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error importing {title}: {e}'))

    def build_api_url(self, title):
        encoded_title = "+".join(title.split())
        return f"{self.base_url}{encoded_title}"

    @staticmethod
    def fetch_data(api_url):
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def extract_movie_data(data):
        genre_names = data.get('Genre', '').split(', ')
        genres = [Genre.objects.get_or_create(name=genre)[0] for genre in genre_names]

        director_name = data.get('Director', '')
        director, _ = Person.objects.get_or_create(name=director_name, specialization=Person.DIRECTOR)

        actors_data = data.get('Actors', '').split(', ')
        actors = [Person.objects.get_or_create(name=actor, specialization=Person.ACTOR)[0] for actor in actors_data]

        return {
            'title': data.get('Title', ''),
            'description': data.get('Plot', ''),
            'duration': int(data.get('Runtime', '').split()[0]) if data.get('Runtime') else None,
            'year': int(data.get('Year', '')) if data.get('Year') else None,
            'director': director,
            'genres': genres,
            'actors': actors
        }

    @staticmethod
    def create_movie(movie_data):
        movie, _ = Movie.objects.get_or_create(
            title=movie_data['title'],
            description=movie_data['description'],
            duration=movie_data['duration'],
            year=movie_data['year'],
            director=movie_data['director']
        )
        movie.genres.set(movie_data['genres'])
        movie.actors.set(movie_data['actors'])
