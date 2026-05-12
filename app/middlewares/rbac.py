from flask import request, jsonify

def require_role(allowed_roles):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            role = request.headers.get("x-user-role")

            if not role:
                return jsonify({"error": "Missing role"}), 401

            if role not in allowed_roles:
                return jsonify({"error": "Forbidden"}), 403

            return fn(*args, **kwargs)

        wrapper.__name__ = fn.__name__
        return wrapper
    return decorator