from app.repositories.customer_repository import create_customer

def create_customer_service(data):
    return create_customer(data)