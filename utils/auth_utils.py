import jwt #pyjwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config import settings
from datetime import datetime, timedelta, timezone
import bcrypt
import utils.storage_utils as storage_utils
from schemas import TokenData
from utils import storage_utils


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_tokens(data: dict):
    access_to_encode = data.copy()
    access_expire_time = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_to_encode.update({"exp": access_expire_time})
    access_token = jwt.encode(access_to_encode, settings.SECRET_KEY, algorithm="HS256")

    refresh_to_encode = data.copy()
    refresh_expire_time = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_to_encode.update({"exp": refresh_expire_time})
    refresh_token = jwt.encode(refresh_to_encode, settings.SECRET_KEY, algorithm="HS256")


    return access_token, refresh_token




def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        #Dekodowanie tokena
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username: str = decoded_token.get("username")
        user_id : int = decoded_token.get("user_id")
        if username is None:
            raise credentials_exception
        if user_id is None:
            raise credentials_exception

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Signature expired. Please log in again.")
    except jwt.InvalidTokenError:
        raise credentials_exception
    except Exception:
        raise credentials_exception

    user = storage_utils.get_user_by_username(username)

    if user is None:
        raise credentials_exception

    return user