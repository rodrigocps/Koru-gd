from flask import request, render_template
from app.services import empresaService as service

EMPRESAS_ENDPOINT = "/api/empresas/"

class EmpresaController:
    def register_routes(app):
        @app.route(EMPRESAS_ENDPOINT, methods=["POST"])
        def save_empresa():
            return service.saveEmpresa(request.json)
        
        @app.route(EMPRESAS_ENDPOINT, methods=["GET"])
        def list_empresas():
            pagina = request.args.get("pagina", default=1, type=int)
            search = request.args.get("search", default=None, type=str)

            return service.listarEmpresas(pagina, search);

        @app.route(EMPRESAS_ENDPOINT + "<int:empresaId>", methods=["GET"])
        def find_empresa(empresaId):
            return service.getEmpresa(empresaId)
         
        ################## FRONTEND ################## 

        @app.route("/empresas/", methods=["GET"])
        def pagina_empresa():
            id = request.args.get("id", default=None, type=int)
            return render_template("empresa.html", empresaId=id)
        