from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer

movie_router = APIRouter()


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=20)
    overview: str = Field(min_length=30, max_length=35)
    year: int = Field(ge=1906, le=2023)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=3, max_length=10)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Movie name",
                "overview": "Overview Overview Overview Overview",
                "year": 2023,
                "rating": 10,
                "category": "Drama"
            }
        }


@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def getMovies() -> List[Movie]:
    db = Session()
    result = jsonable_encoder(db.query(MovieModel).all())
    if not result:
        return JSONResponse(status_code=404, content={"message": "We have not found movies :("})

    return JSONResponse(status_code=200, content=result)


@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
def getMovie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    movie = jsonable_encoder(
        db.query(MovieModel).filter(MovieModel.id == id).first())
    if not movie:
        return JSONResponse(status_code=404, content={"message": "We have a problem in this moment."})

    return JSONResponse(status_code=200, content=movie)


@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200)
def getMovieByCategory(category: str = Query(min_length=4, max_length=10)) -> List[Movie]:
    db = Session()
    listMovie = jsonable_encoder(db.query(MovieModel).filter(
        MovieModel.category == category).all())
    if not listMovie:
        return JSONResponse(status_code=404, content={"message": "Have not been found movies for this category"})

    return JSONResponse(status_code=200, content=listMovie)


@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def createMovie(movie: Movie) -> dict:
    db = Session()
    newMovie = MovieModel(**movie.dict())
    db.add(newMovie)
    db.commit()
    # movies.append(movie)
    return JSONResponse(status_code=201, content={"message": f"The movie '{movie.title}' has been saved."})


@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def updateMovie(id: int, movie: Movie) -> dict:
    db = Session()
    movieO = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not movieO:
        return JSONResponse(status_code=404, content={"message": "Movie hasn't been found."})

    movieO.title = movie.title
    movieO.overview = movie.overview
    movieO.year = movie.year
    movieO.rating = movie.rating
    movieO.category = movie.category
    db.commit()
    return JSONResponse(status_code=200, content={"message": "The movie has been updated."})


@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def deleteMovie(id: int) -> dict:
    db = Session()
    movie = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not movie:
        return JSONResponse(status_code=404, content={"message": "Movie hasn't been found."})

    name = movie.title
    db.delete(movie)
    db.commit()
    return JSONResponse(status_code=200, content={"message": f"{name} has been deleted."})
