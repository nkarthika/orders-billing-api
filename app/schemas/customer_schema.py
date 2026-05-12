from marshmallow import Schema, fields, validate

class CustomerSchema(Schema):
    account_name = fields.Str(required=True)
    state = fields.Str()
    channel = fields.Str(validate=validate.OneOf(["DIRECT", "OEM"]))
    sales_rep = fields.Str()