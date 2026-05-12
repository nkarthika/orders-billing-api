from flask import Blueprint, request, jsonify
from app.services.customer_service import create_customer_service
from app.schemas.customer_schema import CustomerSchema
from app.middlewares.rbac import require_role

customer_bp = Blueprint("customer", __name__)
schema = CustomerSchema()

@customer_bp.route("/", methods=["POST"])
@require_role(["SALES"])
def create_customer():
    data = request.get_json()

    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    customer = create_customer_service(data)

    return jsonify({"customer_id": customer.id}), 201