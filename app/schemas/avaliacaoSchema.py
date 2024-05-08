from marshmallow import Schema, fields, validate

class AvaliacaoSchema(Schema):
    id = fields.Integer(required=True, dump_only=True)
    titulo = fields.String(required=True, validate=validate.Length(min=4, max=50))
    texto = fields.String(required=True, validate=validate.Length(min=10, max=256))
