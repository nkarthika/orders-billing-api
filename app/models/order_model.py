from app import db
import uuid
from datetime import datetime, timezone

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = db.Column(db.String, db.ForeignKey("customers.id"), nullable=False)
    amount = db.Column(db.Numeric, nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default="CREATED")
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))