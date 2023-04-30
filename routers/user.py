from fastapi import APIRouter
from fastapi.responses import JSONResponse
from jwt_manager import createToken
from schemas.user import User


user_router = APIRouter()



@user_router.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "correo@correo.com" and user.password == "kokoro":
        token: str = createToken(user.dict())
        return JSONResponse(status_code=200, content=token)
    else:
        return JSONResponse(status_code=404, content={"message": "email or password not valid."})
