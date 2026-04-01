from sqlalchemy import Integer, String, Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base

class Cart_Class(Base):
    __tablename__="Cart_Table"

    user_id = Column(Integer, ForeignKey('User_Table.user_id'))
    order_id = Column(Integer, ForeignKey('Order_Table.order_id'))
    item_id = Column(Integer, ForeignKey('Item_Table.item_id'))
    item_quantity = Column(Integer, nullable=False)

    items = relationship("Items", back_populates="cart")
    orders = relationship("Orders", back_populates="cart") 