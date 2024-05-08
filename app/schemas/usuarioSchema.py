from marshmallow import Schema, fields, validate

class UsuarioSchema(Schema):
    id = fields.Integer(required=True, dump_only=True)
    nome = fields.String(required=True, validate=validate.Length(min=2, max=100))
    email = fields.String(required=True, validate=validate.Length(min=8))
    senha = fields.String(required=True, validate=validate.Length(min=8))

    