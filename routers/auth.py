from fastapi import  Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

import utils.storage_utils as storage_utils
from schemas import  Token
from utils.auth_utils import verify_password,create_access_token

router = APIRouter(
    tags=["auth"]
)


@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = storage_utils.get_user_by_username(form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='UNAUTHORIZED, INCORRECT PASSWORD OR USERNAME',
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"username": user.username, "user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}