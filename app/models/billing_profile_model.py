from app import db
import uuid
from datetime import datetime, timezone

class BillingProfile(db.Model):
    __tablename__ = "billing_profiles"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = db.Column(db.String, db.ForeignKey("customers.id"), unique=True, nullable=False)
    billing_number = db.Column(db.String, unique=True, nullable=False)
    billing_frequency = db.Column(db.String(20), default="MONTHLY")
    #billing_period_start = db.Column(db.Date)
    #billing_period_end = db.Column(db.Date)
    currency = db.Column(db.String(10))
    status = db.Column(db.String(20), default="ACTIVE")
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    last_billed_at = db.Column(db.DateTime, nullable=True)
    total_orders = db.Column(db.Integer, default=0)