from app.models.billing_profile_model import BillingProfile
from app import db

def get_billing_by_customer(customer_id):
    return BillingProfile.query.filter_by(customer_id=customer_id).first()

def create_billing_profile(data):
    billing = BillingProfile(**data)
    db.session.add(billing)
    db.session.commit()
    return billing