from app import db
import uuid

class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    account_name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50))
    channel = db.Column(db.String(20))
    sales_rep = db.Column(db.String(100))