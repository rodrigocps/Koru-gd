from flask import request, render_template
from app.services import usuarioService as service, authService

USUARIOS_ENDPOINT = "/api/usuarios/"

'''
1- Qual a página inicial?
2- Quais páginas só serão acessadas caso o usuário eseteja logado?
3- controlo o logout de usuarioService aqui
'''
'''
register:
1- Uso um session.clear() nessa página ?
2- return Redirecionar para index?
3- Criar um if else para o o método get renderizar a página de login novamente

login:
1 - Uso um session.clear() nessa página ?
'''
class UsuarioController:
    def register_routes(app):
        @app.route(USUARIOS_ENDPOINT, methods=["POST"])
        def create_usuario():
            return service.adicionarUsuario(request.json)
        
        @app.route(USUARIOS_ENDPOINT + "auth", methods=["POST"])
        def login_usuario():
            return service.login(request.json)
        
        # @app.route(USUARIOS_ENDPOINT + "<int:id>", methods=["GET"])
        # def get_usuario(id):
        #     return service.getUsuario(id)
        
        @app.route(USUARIOS_ENDPOINT + "logout", methods = ["POST"])
        def logout_usuario():
            return service.logout()
        
        @app.route(USUARIOS_ENDPOINT + "validate", methods = ["GET"])
        def validate_usuario():
            return authService.validateLogin()
        ################## FRONTEND ################## 
        
        @app.route("/signup", methods=["GET"])
        def registro():
            return render_template("registro.html")
        
        @app.route("/login", methods=["GET"])
        def login():
            return render_template("login.html")
        
        
        # Perfil de usuário

        # @app.route("/perfil", methods=["GET"])
        # def perfil():
        #     return render_template("perfil.html")
