from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "API Movie"
app.version = '1.0'

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


@app.get('/movies', tags=['movies'])
def getMovies():
    return movies


@app.get('/movies/{id}', tags=['movies'])
def getMovie(id: int):
    movie = list(filter(lambda x: x['id'] == id, movies))
    # print(movie)
    return movie


@app.get('/movies/', tags=['movies'])
def getMovieByCategory(category: str, year: int):
    listMovie = list(filter(lambda movie: movie['category'] == category or int(
        movie['year']) == year, movies))
    return listMovie


@app.post('/movies', tags=['movies'])
def createMovie(id: int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    movies.append({
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
    })
    return movies


@app.put('/movies/{id}', tags=['movies'])
def updateMovie(id: int, title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    movie = list(filter(lambda m: m['id'] == id, movies))
    movie[0]['title'] = title
    movie[0]['overview'] = overview
    movie[0]['year'] = int(year)
    movie[0]['rating'] = float(rating)
    movie[0]['category'] = category
    return movies


@app.delete('/movies/{id}',tags=['movies'])
def deleteMovie(id:int):
    movie = list(filter(lambda m: m['id'] == id, movies))
    movies.remove(movie[0])
    return movies
