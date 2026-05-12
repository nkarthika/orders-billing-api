from flask import Blueprint, jsonify, request
from app.services.billing_service import get_billing_profile
from app.schemas.billing_schema import BillingResponseSchema
from app.middlewares.rbac import require_role

billing_bp = Blueprint("billing", __name__)
schema = BillingResponseSchema()

@billing_bp.route("/<customer_id>", methods=["GET"])
@require_role(["FINANCE"])
def get_billing(customer_id):
    #role = request.headers.get("x-user-role")
    #if role != "FINANCE":
    #    return jsonify({"error": "Unauthorized"}), 403

    billing = get_billing_profile(customer_id)

    if not billing:
        return jsonify({"error": "Not found"}), 404

    return jsonify(schema.dump(billing)), 200

#get_billing = billing_bp.route("/<customer_id>", methods=["GET"])(get_billing)