from flask import request
from app.services import usuarioService as service
from app.schemas.schemasValidation import validate, getUsuarioSchema

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