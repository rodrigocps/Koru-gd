from flask import request
from app.services import avaliacaoService as service

AVALIACOES_ENDPOINT = "/empresas/<int:empresaId>/avaliacoes/"

class Avaliacao:
    def register_routes(app):
        @app.route(AVALIACOES_ENDPOINT, methods=['POST'])
        def create_avaliacao(empresaId):
            avaliacao = request.json
            return service.adicionarAvaliacao(avaliacao, empresaId)

        @app.route(AVALIACOES_ENDPOINT, methods=['GET'])
        def list_avaliacao(empresaId):
            return service.getAvaliacoes(empresaId)
        
        @app.route(AVALIACOES_ENDPOINT + "<int:avaliacaoId>", methods=['GET'])
        def find_avaliacao(empresaId, avaliacaoId):
            return service.getAvaliacao(empresaId, avaliacaoId)
        
        @app.route(AVALIACOES_ENDPOINT + "<int:avaliacaoId>", methods=['PUT'])
        def update_avaliacao(empresaId, avaliacaoId):
            avaliacao = request.json
            return service.editarAvaliacao(empresaId, avaliacaoId, avaliacao) 
        
        @app.route(AVALIACOES_ENDPOINT + "<int:avaliacaoId>", methods=['DELETE'])
        def delete_avaliacao(empresaId, avaliacaoId):
            return service.excluirAvaliacao(empresaId, avaliacaoId)
        
