from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base

class Restaurent_Class(Base):
    __tablename__="Restaurent_Table"

    Restaurent_id = Column(Integer, nullable=False, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("User_Table.user_id"), nullable=False, index=True)
    Restaurent_name = Column(String, nullable=False)
    Restaurent_address = Column(String, nullable=False)
    Restaurent_phone = Column(String, nullable=False)
    Restaurent_rating = Column(Integer, nullable=False, index=True)

    owner = relationship("User_Class", back_populates="owned_restaurents")
    menu = relationship("Menu_Class", back_populates="restaurent", cascade="all, delete-orphan")
