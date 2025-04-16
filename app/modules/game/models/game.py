from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.core.database import Base
from enum import Enum as PyEnum

class UserLearnPath(Base):
    __tablename__ = 'user_learn_path'

class User(Base):
    __tablename__ = "users"

    userid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    account_status = Column(Enum(AccountStatus), default=AccountStatus.ACTIVE)
    role = Column(Enum(UserRole), default=UserRole.STUDENT)
