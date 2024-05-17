from marshmallow import Schema, fields, validate
from marshmallow.exceptions import ValidationError
from flask import abort, jsonify
from .models import Avaliacao, Empresa, Usuario
from app import db

class AvaliacaoSchema(Schema):
    class Meta:
        model = Avaliacao
        sqla_session = db.session
    id = fields.Integer()
    titulo = fields.String(validate = validate.Length(min=8, max=100))
    texto = fields.String(validate = validate.Length(min=10, max=255))

class EmpresaSchema(Schema):
    class Meta:
        model = Empresa
        sqla_session = db.session
    id = fields.Integer()
    nome = fields.String()
    setor = fields.String()
    logo_url = fields.String()

class UsuarioSchema(Schema):
    class Meta:
        model = Usuario
        sqla_session = db.session
    id = fields.Integer()
    nome = fields.String()
    email = fields.Email()
    senha = fields.String()

class UsuarioLoginSchema(Schema):
    class Meta:
        model = Usuario
        sqla_session = db.session
    email = fields.Email()
    senha = fields.String()

def validate(json, schema):
    try:
        data = schema.load(json)
    except ValidationError as e:
        resposta = jsonify({
            "messagem" : "Erro de validação.",
            "erros" : e.messages
        })
        resposta.status_code = 422
        
        return abort(resposta)
    return data