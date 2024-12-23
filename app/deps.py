from fastapi import Depends, HTTPException, status, Header
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from .utils import SECRET_KEY, ALGORITHM
from .schemas import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(authorization: str = Header(None), token: str = Depends(oauth2_scheme)) -> User:
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is missing")
    try:
        token = authorization.split(" ")[1] if authorization else None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
    return User(email=username, password="")
