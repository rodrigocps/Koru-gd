from flask import request, render_template
from app.services import empresaService as service

EMPRESAS_ENDPOINT = "/empresas/"

class Empresa:
    def register_routes(app):
        @app.route(EMPRESAS_ENDPOINT, methods=["GET"])
        def list_empresas():
            id = request.args.get("id", default=None, type=int)
            pagina = request.args.get("pagina", default=1, type=int)
            search = request.args.get("search", default=None, type=str)

            if id:
                ################## FRONTEND ################## 
                return render_template("empresa.html", empresaId=id)
            else:
                return service.listarEmpresas(pagina, search);

        @app.route(EMPRESAS_ENDPOINT + "<int:empresaId>", methods=["GET"])
        def find_empresa(empresaId):
            return service.getEmpresa(empresaId)
        
         
        