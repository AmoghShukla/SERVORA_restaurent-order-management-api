from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.database.base import Base
from datetime import datetime

class Order_Class(Base):
    __tablename__ = "Orders_Table"

    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('User_Table.user_id'))
    order_status = Column(String)
    payment_status = Column(String)
    total_amount = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship('User_Class', back_populates="orders")
    items = relationship('Items_Class', secondary='OrderItems_Table', back_populates="orders", viewonly=True)
    order_items = relationship('OrderItems_Class', back_populates="order")
    

