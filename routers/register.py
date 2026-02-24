from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import storage
import utils.storage_utils as storage_utils
from schemas import User, UserInDB, UserCreate, Token, TokenData
from utils.auth_utils import get_password_hash, verify_password,create_access_token

router = APIRouter(
    prefix="/register",
    tags=["register"],
)

@router.post("/", response_model=User)
def register_user(user: UserCreate):
    print(f"DEBUG: Hasło: {user.password}, Typ: {type(user.password)}")
    db_user = storage_utils.get_user_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    hashed_password = get_password_hash(user.password)
    new_user = storage_utils.save_user(user, hashed_password)
    return new_user

