from flask import abort, jsonify
from app.schemas import avaliacaoSchema, usuarioSchema 
from marshmallow import ValidationError

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
    
def getAvaliacaoSchema():
    return avaliacaoSchema.AvaliacaoSchema()

def getUsuarioSchema():
    return usuarioSchema.UsuarioSchema()