from sqlalchemy.orm import relationship
from sqlalchemy import Integer, Float, String, Column, DateTime
from src.database.base import Base
from datetime import datetime
from sqlalchemy import Enum
import enum

class UserRole(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    RESTAURANT_OWNER = "RESTAURANT_OWNER"

class User_Class(Base):
    __tablename__ = "User_Table"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String)
    user_email = Column(String, unique=True)
    user_password = Column(String)
    user_phone = Column(String)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime, default=datetime.now())

    orders = relationship("Order_Class", back_populates="user")
    owned_restaurents = relationship("Restaurent_Class", back_populates="owner")