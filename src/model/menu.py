from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Column, ForeignKey
from src.database.base import Base

class Menu_Class(Base):
    __tablename__="Menu_Table"

    cuisine_id = Column(Integer, nullable=False, primary_key=True)
    cuisine_name = Column(String, nullable=False)
    restaurent_id = Column(Integer, ForeignKey("Restaurent_Table.Restaurent_id"), nullable=False, index=True)

    restaurent = relationship("Restaurent_Class", back_populates="menu")
    items = relationship("Items_Class", back_populates="menu", cascade="all, delete-orphan")

    