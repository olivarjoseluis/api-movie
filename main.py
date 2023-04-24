from fastapi import FastAPI
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.auth import auth_router


app = FastAPI()
app.title = "API Movie"
app.version = '1.0'

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)


@app.get('/', tags=['home'])
def message():
    return 'Welcome to API Movie'
