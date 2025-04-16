from sqlalchemy.orm import Session
from app.modules.user.models.user import User
from app.modules.user.schemas.schemas import UserCreate
from app.utils.logger import get_logger
import bcrypt

logger = get_logger("user-services.py")

def create_user(db: Session, user_data: UserCreate):
    logger.info("Creating User")
    hashed_password = bcrypt.hashpw(user_data.password.encode(), bcrypt.gensalt()).decode()
    new_user = User(username=user_data.username, email=user_data.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"User created: {new_user.username}")
    return new_user

def get_user(db: Session, user_id: str):
    logger.info("Retrieving User")

    return db.query(User).filter(User.userid == user_id).first()

def get_all_users(db: Session):
    logger.info("Retrieving all Users")

    return db.query(User).all()

def update_user(db: Session, user_id: str, update_data: dict):
    logger.info("Updating User")

    user = db.query(User).filter(User.userid == user_id).first()
    if not user:
        return None
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: str):
    logger.info("Deleting User")

    user = db.query(User).filter(User.userid == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
