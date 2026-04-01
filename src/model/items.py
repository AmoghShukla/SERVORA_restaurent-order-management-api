from sqlalchemy import Integer, String, Boolean, Column
from sqlalchemy.orm import relationship
from src.database.base import Base

class Items_Class(Base):
    __tablename__="Items_Table"

    item_id = Column(Integer, primary_key=True, index=True, nullable=False)
    item_name = Column(String, nullable=False)
    item_price = Column(Integer, nullable=False)
    item_rating = Column(Integer, nullable=False)
    item_availability = Column(Boolean, nullable=False)

    orders = relationship('Orders_Class', back_populates="items")
    cart = relationship('Cart_Class', secondary='Cart_Table',back_populates="items")