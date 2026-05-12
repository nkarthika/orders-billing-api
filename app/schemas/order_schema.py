from marshmallow import Schema, fields, validate

class OrderSchema(Schema):
    customer_id = fields.Str(required=True)
    amount = fields.Float(required=True)
    currency = fields.Str(required=True)