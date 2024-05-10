from flask import request, render_template
from app.services import usuarioService as service
from app.schemas.schemasValidation import validate, getLoginSchema, getUsuarioSchema

USUARIOS_ENDPOINT = "/usuarios/"

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
class Usuario:
    def register_routes(app):
        @app.route(USUARIOS_ENDPOINT, methods=["POST"])
        def create_usuario():
            usuario = validate(request.json, getUsuarioSchema())
            return service.adicionarUsuario(usuario)
        
        @app.route(USUARIOS_ENDPOINT + "auth", methods=["POST"])
        def login_usuario():
            login = validate(request.json, getLoginSchema())
            return service.login(login)
        
        @app.route(USUARIOS_ENDPOINT + "<int:id>")
        def get_usuario(id):
            return service.getUsuario(id)
        
        def logout_usuario():
            return service.logout()
        
        ## FRONTEND ##
        @app.route("/signup", methods=["GET"])
        def registro():
            return render_template("registro.html")
        
        # Perfil de usuário

        # @app.route("/perfil", methods=["GET"])
        # def perfil():
        #     return render_template("perfil.html")
