from flask import Blueprint, request, jsonify
from app.services.order_service import create_order_service
from app.schemas.order_schema import OrderSchema
from app.middlewares.rbac import require_role

order_bp = Blueprint("order", __name__)
schema = OrderSchema()

@order_bp.route("/", methods=["POST"])
@require_role(["SALES"])
def create_order():
    data = request.get_json()

    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    order, billing_created = create_order_service(data)

    return jsonify({
        "order_id": order.id,
        "status": order.status,
        "billing_profile_created": billing_created
    }), 201