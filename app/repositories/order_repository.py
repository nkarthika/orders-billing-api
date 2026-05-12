from app.models.order_model import Order
from app import db

def create_order(data):
    order = Order(**data)
    db.session.add(order)
    db.session.commit()
    return order