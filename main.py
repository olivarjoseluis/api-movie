from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "API Movie"
app.version = '1.0'


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=20)
    overview: str = Field(min_length=30, max_length=35)
    year: int = Field(ge=1906, le=2023)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=4, max_length=10)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Movie name",
                "overview": "Overview Overview Overview Overview",
                "year": 2024,
                "rating": 10,
                "category": "Drama"
            }
        }


movies = [
    {
        'id': 1,
        'title': 'The Shawshank Redemption',
        'overview': "Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion.",
        'year': '1994',
        'rating': 9.3,
        'category': 'Drama'
    },
    {
        'id': 2,
        'title': 'The Godfather',
        'overview': 'The aging patriarch of an organized crime dynasty in postwar New York City transfers control of his clandestine empire to his reluctant youngest son.',
        'year': '1972',
        'rating': 9.2,
        'category': 'Crime'
    },
    {
        'id': 3,
        'title': 'The Dark Knight',
        'overview': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
        'year': '2008',
        'rating': 9.0,
        'category': 'Action'
    },
    {
        'id': 4,
        'title': 'The Godfather Part II',
        'overview': 'The early life and career of Vito Corleone in 1920s New York City is portrayed, while his son, Michael, expands and tightens his grip on the family crime syndicate.',
        'year': '1974',
        'rating': 9.0,
        'category': 'Crime'
    },
    {
        'id': 5,
        'title': '12 Angry Men',
        'overview': 'The jury in a New York City murder trial is frustrated by a single member whose skeptical caution forces them to more carefully consider the evidence before jumping to a hasty verdict.',
        'year': '1957',
        'rating': 9.0,
        'category': 'Drama'
    },
    {
        'id': 6,
        'title': "Schindler's List",
        'overview': 'In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis.',
        'year': '1993',
        'rating': 9.0,
        'category': 'History'
    },
    {
        'id': 7,
        'title': 'The Lord of the Rings: The Return of the King',
        'overview': "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.",
        'year': '2003',
        'rating': 9.0,
        'category': 'Adventure'
    },
    {
        'id': 8,
        'title': 'Pulp Fiction',
        'overview': 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.',
        'year': '1994',
        'rating': 8.9,
        'category': 'Crime'
    },
    {
        'id': 9,
        'title': 'The Lord of the Rings: The Fellowship of the Ring',
        'overview': 'A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.',
        'year': '2001',
        'rating': 8.8,
        'category': 'Action'
    },
    {
        'id': 10,
        'title': 'The Good, the Bad and the Ugly',
        'overview': 'A bounty hunting scam joins two men in an uneasy alliance against a third in a race to find a fortune in gold buried in a remote cemetery.',
        'year': '1966',
        'rating': 8.8,
        'category': 'Adventure'
    }
]


@app.get('/', tags=['home'])
def message():
    return 'Hello world'


@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200)
def getMovies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)


@app.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
def getMovie(id: int = Path(ge=1, le=2000)) -> Movie:
    movie = list(filter(lambda x: x['id'] == id, movies))
    if (len(movie) > 0):
        return JSONResponse(status_code=200, content=movie)
    else:
        return JSONResponse(status_code=404, content={"message": "We have a problem in this moment."})


@app.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200)
def getMovieByCategory(category: str = Query(min_length=5, max_length=10)) -> List[Movie]:
    listMovie = list(
        filter(lambda movie: movie['category'] == category, movies))
    if (len(listMovie) > 0):
        return JSONResponse(status_code=200, content=listMovie)
    else:
        return JSONResponse(status_code=404, content={"message": "Have not been found movies for this category"})


@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def createMovie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201, content={"message": f"The movie '{movie.title}' has been saved."})


@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def updateMovie(id: int, movie: Movie) -> dict:
    movieO = list(filter(lambda m: m['id'] == id, movies))
    if (len(movieO) > 0):
        movieO[0]['title'] = movie.title
        movieO[0]['overview'] = movie.overview
        movieO[0]['year'] = movie.year
        movieO[0]['rating'] = movie.rating
        movieO[0]['category'] = movie.category
        return JSONResponse(status_code=200, content={"message": "The movie has been updated."})
    else:
        return JSONResponse(status_code=404, content={"message": "Movie hasn't been found."})


@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def deleteMovie(id: int) -> dict:
    movie = list(filter(lambda m: m['id'] == id, movies))
    if (len(movie) > 0):
        name = movie[0]['title']
        movies.remove(movie[0])
        return JSONResponse(status_code=200, content={"message": f"{name} has been deleted."})
    else:
        return JSONResponse(status_code=404, content={"message": "Movie hasn't been found."})
