from schemas import UserInDB, UserCreate, Task, TaskCreate
from typing import Optional
import storage
from schemas import UserInDB, UserCreate


def get_user_by_username(username: str) -> Optional[UserInDB]:
    for user in storage.fake_users_db:
        if user.username == username:
            return user
    return None

def save_user(user: UserCreate, hashed_password: str) -> UserInDB:

    user_data = user.model_dump()

    user_data.pop("password")

    new_id = len(storage.fake_users_db) +  1

    new_user = UserInDB(
        **user_data,
        hashed_password = hashed_password,
        id = new_id
    )
    storage.fake_users_db.append(new_user)
    return new_user