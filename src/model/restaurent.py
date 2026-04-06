from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
from src.database.base import Base
from src.model.menu import Menu_Class

class Restaurent_Class(Base):
    __tablename__="Restaurent_Table"

    Restaurent_id = Column(Integer, nullable=False, primary_key=True, index=True)
    Restaurent_name = Column(String, nullable=False)
    Restaurent_address = Column(String, nullable=False)
    Restaurent_phone = Column(Integer, nullable=False)
    Restaurent_rating = Column(Integer, nullable=False, index=True)

    menu = relationship("Menu_Class", back_populates="restaurent")
