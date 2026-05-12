from flask import jsonify
from app.utils.errors import NotFoundError, ValidationError

def register_error_handlers(app):

    @app.errorhandler(NotFoundError)
    def handle_not_found(error):
        return jsonify({
            "error": "NOT_FOUND",
            "message": str(error)
        }), 404


    @app.errorhandler(ValidationError)
    def handle_validation(error):
        return jsonify({
            "error": "VALIDATION_ERROR",
            "message": str(error)
        }), 400


    @app.errorhandler(Exception)
    def handle_generic(error):
        return jsonify({
            "error": "INTERNAL_ERROR",
            "message": "Something went wrong"
        }), 500