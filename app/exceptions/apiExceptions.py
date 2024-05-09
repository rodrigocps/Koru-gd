from flask import abort, jsonify

def getJsonifiedResponseWithStatusCode(response, statusCode):
    response = jsonify(response)
    response.status_code = statusCode
    return response

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
def throwUpdateAvaliacaoException():
    return throwCreateException({
        "mensagem" : "Houve uma falha ao atualizar a avaliação."
    })

def throwUpdateUsuarioException():
    return throwCreateException({
        "mensagem" : "Houve uma falha ao atualizar o usuário."
    })

################## DELETE EXCEPTIONS ##################

def throwDeleteAvaliacaoException():
    return throwCreateException({
        "mensagem" : "Houve uma falha ao excluir a avaliação."
    })

def throwDeleteUsuarioException():
    return throwCreateException({
        "mensagem" : "Houve uma falha ao excluir o usuário."
    })
