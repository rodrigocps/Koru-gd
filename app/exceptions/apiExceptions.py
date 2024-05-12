from flask import abort, jsonify

def getJsonifiedResponseWithStatusCode(response, statusCode):
    response = jsonify(response)
    response.status_code = statusCode
    return response

################## AUTH EXCEPTIONS ##################
def throwUnauthorizedException(response):
    return abort(getJsonifiedResponseWithStatusCode(response, 401))

def throwUserNotAuthenticatedException():
    throwUnauthorizedException({
        "mensagem" : "O usuário deve estar logado para executar essa operação."
    })


################## CREATE EXCEPTIONS ##################
def throwCreateException(response):
    return abort(getJsonifiedResponseWithStatusCode(response, 400))

def throwCreateAvaliacaoException():
    return throwCreateException({
        "mensagem" : "Houve uma falha ao salvar a avaliação."
    })

def throwCreateUsuarioException():
    return throwCreateException({
        "mensagem" : "Houve uma falha ao cadastrar usuário."
    })
#IAN
def throwUsuarioExistente():
    return throwCreateException({
        "mensagem" : "Usuário já cadastrado."
    })

################## READ EXCEPTIONS ##################
def throwNotFoundException(response):
    return abort(getJsonifiedResponseWithStatusCode(response, 404))

def throwAvaliacaoNotFoundException():
    return throwNotFoundException({
        "messagem" : "Avaliação não encontrada."
    })

def throwUsuárioNotFoundException():
    return throwNotFoundException({
        "messagem" : "Usuário não encontrado."
    })

def throwEmpresaNotFoundException():
    return throwNotFoundException({
        "messagem" : "Empresa não encontrada."
    })

################## UPDATE EXCEPTIONS ##################
def throwUpdateException(response):
    return abort(getJsonifiedResponseWithStatusCode(response, 400))

def throwUnauthorizedUpdateException(response):
    return abort(getJsonifiedResponseWithStatusCode(response, 401))

def throwUpdateAvaliacaoException():
    return throwCreateException({
        "mensagem" : "Houve uma falha ao atualizar a avaliação."
    })

def throwUnauthorizedUpdateAvaliacaoException():
    return throwUnauthorizedUpdateException({
        "mensagem" : "Somente o autor da avaliação pode alterá-la."
    })

def throwUpdateUsuarioException():
    return throwCreateException({
        "mensagem" : "Houve uma falha ao atualizar o usuário."
    })

################## DELETE EXCEPTIONS ##################
def throwDeleteException(response):
    return abort(getJsonifiedResponseWithStatusCode(response, 400))

def throwUnauthorizedDeleteException(response):
    return abort(getJsonifiedResponseWithStatusCode(response, 401))

def throwDeleteAvaliacaoException():
    return throwDeleteException({
        "mensagem" : "Houve uma falha ao excluir a avaliação."
    })

def throwDeleteAvaliacaoException():
    return throwDeleteException({
        "mensagem" : "Houve uma falha ao excluir a avaliação."
    })

def throwUnauthorizedDeleteAvaliacaoException():
    return throwUnauthorizedDeleteException({
        "mensagem" : "Somente o autor da avaliação pode deletá-la."
    })

def throwDeleteUsuarioException():
    return throwDeleteException({
        "mensagem" : "Houve uma falha ao excluir o usuário."
    })
    
