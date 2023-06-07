from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True)
    bot_name = Column(String, index=True)
    ex_name = Column(String, index=True)
    symbol = Column(String, index=True)
    base = Column(String, index=True)
    quote = Column(String, index=True)
    action = Column(String, index=True)
    type = Column(String, index=True)
    side = Column(String, index=True)
    price = Column(Float, index=True)
    avg_price = Column(Float, index=True)
    status = Column(String, index=True)
    ori_qty = Column(Float, index=True)
    executed_qty = Column(Float, index=True)
    fee = Column(Float, index=True)
    ts = Column(Integer, index=True)