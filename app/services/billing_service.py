from app.repositories.billing_repository import get_billing_by_customer, create_billing_profile
from datetime import date, timedelta, timezone, datetime
import uuid

def create_billing_if_not_exists(customer_id, currency):
    existing = get_billing_by_customer(customer_id)
    if existing:
        return existing, False

    today = date.today()

    data = {
        "customer_id": customer_id,
        "billing_number": f"INV-{uuid.uuid4().hex[:6]}",
        "billing_frequency": "MONTHLY",
        #"billing_period_start": today,
        #"billing_period_end": today + timedelta(days=30),
        "currency": currency,
        "status": "ACTIVE"
    }

    billing = create_billing_profile(data)
    return billing, True


def get_billing_profile(customer_id):
    return get_billing_by_customer(customer_id)

def update_billing_summary(billing):
    billing.total_orders = billing.total_orders or 0
    billing.total_orders += 1
    billing.last_billed_at = datetime.now(timezone.utc)