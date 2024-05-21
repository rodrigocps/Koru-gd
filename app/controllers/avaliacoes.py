from flask import request
from app.services import avaliacaoService as service

AVALIACOES_ENDPOINT = "/api/empresas/<int:empresaId>/avaliacoes/"

class AvaliacaoController:
    def register_routes(app):
        @app.route(AVALIACOES_ENDPOINT, methods=['POST'])
        def create_avaliacao(empresaId):
            return service.adicionarAvaliacao(request.json, empresaId)

        @app.route(AVALIACOES_ENDPOINT, methods=['GET'])
        def list_avaliacoes(empresaId):
            return service.getAvaliacoes(empresaId)
        
        @app.route("/api/usuarios/avaliacoes", methods=['GET'])
        def list_all_avaliacoes():
            return service.getAllAvaliacoes(request.args)
        
        @app.route(AVALIACOES_ENDPOINT + "<int:avaliacaoId>", methods=['GET'])
        def find_avaliacao(empresaId, avaliacaoId):
            return service.getAvaliacao(empresaId, avaliacaoId)
        
        @app.route(AVALIACOES_ENDPOINT + "<int:avaliacaoId>", methods=['PUT'])
        def update_avaliacao(empresaId, avaliacaoId):
            return service.editarAvaliacao(empresaId, avaliacaoId, request.json) 
        
        @app.route(AVALIACOES_ENDPOINT + "<int:avaliacaoId>", methods=['DELETE'])
        def delete_avaliacao(empresaId, avaliacaoId):
            return service.excluirAvaliacao(empresaId, avaliacaoId)

        
