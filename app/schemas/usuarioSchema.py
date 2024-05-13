from marshmallow import Schema, fields, validate

class UsuarioSchema(Schema):
    id = fields.Integer(required=True, dump_only=True)
    nome = fields.String(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    senha = fields.String(required=True, validate=validate.Length(min=8))

class UsuarioLoginSchema(Schema):
    email = fields.Email(required=True)
    senha = fields.String(required=True, validate=validate.Length(min=8))

