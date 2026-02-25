import jwt
from fastapi import  Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Response
from config import settings
import utils.storage_utils as storage_utils
from schemas import  Token
from utils.auth_utils import verify_password,create_tokens
from fastapi import Cookie
router = APIRouter(
    tags=["auth"]
)


@router.post("/login", response_model=Token)
def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = storage_utils.get_user_by_username(form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='UNAUTHORIZED, INCORRECT PASSWORD OR USERNAME',
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token, refresh_token = create_tokens(data={"username": user.username, "user_id": user.id})

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False, #currently no HTTPS
        samesite="lax", #deffence from CSRF
        max_age=7*24*3600 #7 Days (seconds)
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str = Cookie(None)):
    try :
        decoded_token = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        username : str = decoded_token.get("username")
        user_id  : int = decoded_token.get("user_id")

        new_access_token = create_tokens(data={"username": username, "user_id": user_id})[0]
        return {"access_token": new_access_token, "token_type": "bearer"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token."
        )

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="refresh_token")
    return {"message": "You have been logged out"}