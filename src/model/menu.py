from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Column
from src.database.base import Base

class Menu_Class(Base):
    __tablename__="Menu_Table"

    cuisine_id = Column(Integer, nullable=False, primary_key=True)
    cuisine_name = Column(String, nullable=False)

    