# Movie API


The Movie API is a Django RESTful web service that provides endpoints for managing movies, people (actors and directors), and genres. It allows users to retrieve information about movies, filter movies by various criteria, add new movies, and more. Site is deployed in Render.
---

## Site

- **Main page:** https://movie-api-71ja.onrender.com/
- **Swagger:** https://movie-api-71ja.onrender.com/api/doc/swagger/
- **Admin page:** https://movie-api-71ja.onrender.com/admin/ (username: `admin`, password: `Admin12345`)

---
---

## Features

- **Movies:** CRUD operations for managing movie data including title, description, duration, release year, director, actors, and genres.
- **People:** CRUD operations for managing people data including actors and directors.
- **Genres:** CRUD operations for managing genre data.
- **Filtering:** Filter movies by year, director, actor, and title.
- **Pagination:** Paginated responses for large datasets (default by 25).
- **API Documentation:** Detailed documentation (Swagger) of available endpoints and request/response formats.
- **Data Import:** Command-line `import_data` utility to import movie data from www.omdbapi.com.
- **Testing:** all endpoints and filters are tested by `django.test` tests

---

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/vasylhnatiuk/movie-api.git
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run database migrations:**

    ```bash
    python manage.py migrate
    ```

4. **Start the development server:**

    ```bash
    python manage.py runserver
    ```
5. **Import data from www.omdbapi.com**

    ```bash
    python manage.py import_data
    ```
---

## Usage

- **Endpoints:** Access API endpoints through the following base URL:

    ```
    http://localhost:8000
    ```

- **Authentication:** The API does not require authentication for accessing public endpoints. However, authentication can be added for specific endpoints if needed.

- **API Documentation:** View detailed API documentation and available endpoints by navigating to the following URL in your browser:

    ```
    (http://127.0.0.1:8000/api/doc/swagger/)
    ```

    This provides an interactive API documentation with information about request/response formats, available endpoints, and sample requests.


