from models.movie import Movie as MovieModel
from fastapi.responses import JSONResponse
from schemas.movie import Movie


class MovieService():
    def __init__(self, db) -> None:
        self.db = db

    def create_movie(self, movie:Movie):
        result = ""
        #Propities that will read how parameters
        new_movie = MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        result = JSONResponse(status_code=201, content={
                              "message": f"The movie '{movie.title}' has been saved."})
        return result

    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result

    def get_movie(self, id:int):
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return movie

    def get_movie_by_category(self, category:str):
        list_movies = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return list_movies

    def update_movie(self, id:int, movie:Movie):
        movieO = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        movieO.title = movie.title
        movieO.overview = movie.overview
        movieO.year = movie.year
        movieO.rating = movie.rating
        movieO.category = movie.category
        self.db.commit()
        return

    def delete_movie(self, id:int):
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        self.db.delete(movie)
        self.db.commit()
        return
