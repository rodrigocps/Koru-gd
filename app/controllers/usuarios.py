from flask import request, render_template
from app.services import usuarioService as service
from app.schemas.schemasValidation import validate, getUsuarioSchema

USUARIOS_ENDPOINT = "/usuarios/"

class Usuario:
    def register_routes(app):
        @app.route(USUARIOS_ENDPOINT, methods=["POST"])
        def create_usuario():
            usuario = validate(request.json, getUsuarioSchema())
            return service.adicionarUsuario(usuario)
        
        @app.route(USUARIOS_ENDPOINT + "auth", methods=["POST"])
        def login_usuario(data):
            login = data.json
            return service.login(login)
        
        @app.route(USUARIOS_ENDPOINT + "<int:id>")
        def get_usuario(id):
            return service.getUsuario(id)
        
        def logout_usuario():
            return service.logout()
        
        ## FRONTEND ##
        @app.route("/signup", methods=["GET"])
        def login():
            return render_template("registro.html")
        
        # Perfil de usuário

        # @app.route("/perfil", methods=["GET"])
        # def perfil():
        #     return render_template("perfil.html")
