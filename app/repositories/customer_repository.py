from app.models.customer_model import Customer
from app import db

def create_customer(data):
    customer = Customer(**data)
    db.session.add(customer)
    db.session.commit()
    return customer

def get_customer_by_id(customer_id):
    return Customer.query.filter_by(id=customer_id).first()