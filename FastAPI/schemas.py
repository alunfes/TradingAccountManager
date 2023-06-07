from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrderBase(BaseModel):
    bot_name: str
    ex_name: str
    symbol: str
    base: str
    quote: str
    action: str
    type: str
    side: str
    price: float
    avg_price: float
    status: str
    ori_qty: float
    executed_qty: Optional[float] = None
    fee: float
    ts: int

class OrderCreate(OrderBase):
    pass

class OrderUpdate(OrderBase):
    pass