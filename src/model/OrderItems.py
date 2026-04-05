from sqlalchemy import Integer, Column, ForeignKey, Float
from sqlalchemy.orm import relationship
from src.database.base import Base

class OrderItems_Class(Base):
    __tablename__="OrderItems_Table"

    id = Column(Integer, primary_key=True, index=True)
    
    order_id = Column(Integer, ForeignKey('Orders_Table.order_id'), nullable=False)
    item_id = Column(Integer, ForeignKey('Items_Table.item_id'), nullable=False)

    item_quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    item = relationship("Items_Class", back_populates="order_items")
    order = relationship("Order_Class", back_populates="order_items")