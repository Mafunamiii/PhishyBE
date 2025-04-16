from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.user.schemas.schemas import UserCreate, UserResponse
from app.modules.user.services.services import create_user, get_user, get_all_users, update_user, delete_user
from app.utils.logger import get_logger

router = APIRouter(prefix="/users", tags=["users"])
logger = get_logger("users-routes.py")
@router.post("/", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info("create new user")
    return create_user(db, user)

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: str, db: Session = Depends(get_db)):
    logger.info("read user")
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=list[UserResponse])
def read_all_users(db: Session = Depends(get_db)):
    logger.info("read all users")
    return get_all_users(db)

@router.put("/{user_id}", response_model=UserResponse)
def update_existing_user(user_id: str, update_data: dict, db: Session = Depends(get_db)):
    logger.info("update existing user")
    user = update_user(db, user_id, update_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
def delete_existing_user(user_id: str, db: Session = Depends(get_db)):
    logger.info("delete existing user")
    if not delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
