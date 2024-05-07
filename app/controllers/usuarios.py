from flask import request
from app.services import usuarioService as service

USUARIOS_ENDPOINT = "/usuarios/"

class Usuario:
    def register_routes(app):
        @app.route(USUARIOS_ENDPOINT, methods=["POST"])
        def create_usuario():
            usuario = request.json
            return service.adicionarUsuario(usuario)