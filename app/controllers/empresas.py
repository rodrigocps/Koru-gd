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
            return service.listarEmpresas(request.args);

        @app.route(EMPRESAS_ENDPOINT + "<int:empresaId>", methods=["GET"])
        def find_empresa(empresaId):
            return service.getEmpresa(empresaId)
         
        ################## FRONTEND ################## 

        @app.route("/empresas/", methods=["GET"])
        def pagina_empresa():
            id = request.args.get("id", default=None, type=int)
            return render_template("empresa.html", empresaId=id)
        