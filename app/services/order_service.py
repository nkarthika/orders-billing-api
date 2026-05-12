from app.repositories.order_repository import create_order
from app.services.billing_service import (create_billing_if_not_exists, update_billing_summary)
from app.repositories.customer_repository import get_customer_by_id
from app.utils.errors import NotFoundError
from app import db

def create_order_service(data):
    customer = get_customer_by_id(data["customer_id"])

    if not customer:
        raise NotFoundError("Customer not found")

    order = create_order(data)

    billing, created = create_billing_if_not_exists(
        data["customer_id"],
        data["currency"]
    )
    # NEW: update billing summary
    update_billing_summary(billing)

    db.session.commit()
    return order, created