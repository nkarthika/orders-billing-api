from marshmallow import Schema, fields

class BillingResponseSchema(Schema):
    billing_number = fields.Str()
    billing_frequency = fields.Str()
    #billing_period_start = fields.Date()
    #billing_period_end = fields.Date()
    currency = fields.Str()
    status = fields.Str()
    total_orders = fields.Int()
    last_billed_at = fields.DateTime()