from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base

class Order_Class(Base):
    __tablename__ = "Orders_Table"

    order_id = Column(Integer, primary_key=True, index=True)
    order_status = Column(String)
    payment_status = Column(String)
    total_amount = Column(Integer, nullable=False, index=True)

    user = relationship('User_Class', back_populates="orders")
    items = relationship('Items_Class', back_populates="orders")
    cart = relationship('Cart_Class', secondary='Cart_Table',back_populates="items")
    
    user_id = Column(Integer, ForeignKey('User_Table.user_id'))
    
