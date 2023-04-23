from jwt import encode, decode


def createToken(data: dict):
    token: str = encode(payload=data, key="testing-key", algorithm="HS256")
    return token


def validateToken(token: str) -> dict:
    data: dict = decode(token, key="testing-key", algorithms=['HS256'])
    return data
