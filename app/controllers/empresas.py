from flask import request
from app.services import empresaService as service

EMPRESAS_ENDPOINT = "/empresas/"

class Empresa:
    def register_routes(app):
        @app.route(EMPRESAS_ENDPOINT, methods=["GET"])
        def list_empresas():
            pagina = request.args.get("pagina", default=1, type=int)
            return service.listarEmpresas(pagina);

        @app.route(EMPRESAS_ENDPOINT + "<int:empresaId>", methods=["GET"])
        def find_empresas(empresaId):
            return service.getEmpresa(empresaId)