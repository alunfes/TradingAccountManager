from sqlalchemy.orm import Session
import models, schemas


def get_order(db: Session, order_id: str):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(db: Session, order_id: str, order: schemas.OrderUpdate):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        return None
    for key, value in order.dict().items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: str):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        return None
    db.delete(db_order)
    db.commit()
    return db_order

def delete_order(db: Session, order_id: str):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        return None
    db.delete(db_order)
    db.commit()
    return db_order
