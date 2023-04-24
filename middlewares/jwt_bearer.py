from fastapi import Request, HTTPException
from jwt_manager import validateToken
from fastapi.security import HTTPBearer


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data['email'] != "correo@correo.com":
            raise HTTPException(status_code=403, detail="user forbidden")
