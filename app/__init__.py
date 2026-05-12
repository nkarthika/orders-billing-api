from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #To save memory and avoid warning logs

    db.init_app(app)
    migrate.init_app(app, db)

    from app.controllers.customer_controller import customer_bp
    app.register_blueprint(customer_bp, url_prefix="/api/v1/customers")

    from app.controllers.order_controller import order_bp
    app.register_blueprint(order_bp, url_prefix="/api/v1/orders")

    from app.controllers.billing_controller import billing_bp
    app.register_blueprint(billing_bp, url_prefix="/api/v1/billing-profile")
    
    from app.middlewares.error_handler import register_error_handlers
    register_error_handlers(app)
    
    @app.route("/")
    def home():
        return {"message": "API is running"}
    
    return app