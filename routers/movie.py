from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()




@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def getMovies() -> List[Movie]:
    db = Session()
    result = jsonable_encoder(MovieService(db).get_movies())
    if not result:
        return JSONResponse(status_code=404, content={"message": "We have not found movies :("})

    return JSONResponse(status_code=200, content=result)


@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
def getMovie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    movie = jsonable_encoder(MovieService(db).get_movie(id))
    if not movie:
        return JSONResponse(status_code=404, content={"message": "We have a problem in this moment."})

    return JSONResponse(status_code=200, content=movie)


@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200)
def getMovieByCategory(category: str = Query(min_length=4, max_length=10)) -> List[Movie]:
    db = Session()
    listMovie = jsonable_encoder(MovieService(db).get_movie_by_category(category))
    if not listMovie:
        return JSONResponse(status_code=404, content={"message": "Have not been found movies for this category"})

    return JSONResponse(status_code=200, content=listMovie)


@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def createMovie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={"message": f"The movie '{movie.title}' has been saved."})


@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def updateMovie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "The movie has not been found."})
    
    MovieService(db).update_movie(id,movie)
    return JSONResponse(status_code=200, content={"message": "The movie has been updated."})


@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def deleteMovie(id: int) -> dict:
    db = Session()
    movie = MovieService(db).get_movie(id)
    if not movie:
        return JSONResponse(status_code=404, content={"message": "Movie hasn't been found."})
    
    name = movie.title
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content={"message": f"{name} has been deleted."})
