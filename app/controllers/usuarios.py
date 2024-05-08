from flask import request
from app.services import usuarioService as service
from app.schemas.schemasValidation import validate, getUsuarioSchema

USUARIOS_ENDPOINT = "/usuarios/"

class Usuario:
    def register_routes(app):
        @app.route(USUARIOS_ENDPOINT, methods=["POST"])
        def create_usuario():
            usuario = validate(request.json, getUsuarioSchema())
            return service.adicionarUsuario(usuario)