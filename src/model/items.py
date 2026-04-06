from sqlalchemy import Integer, String, Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base


class Items_Class(Base):
    __tablename__="Items_Table"

    item_id = Column(Integer, primary_key=True, index=True, nullable=False)
    menu_id = Column(Integer, ForeignKey("Menu_Table.cuisine_id"), nullable=False, index=True)
    item_name = Column(String, nullable=False)
    item_price = Column(Integer, nullable=False)
    item_rating = Column(Integer, nullable=False)
    item_availability = Column(Boolean, nullable=False)

    menu = relationship('Menu_Class', back_populates="items")
    orders = relationship('Order_Class', secondary='OrderItems_Table', back_populates="items", viewonly=True)
    order_items = relationship('OrderItems_Class', back_populates="item")