from flask import session, make_response
import app.exceptions.apiExceptions as exceptions


def validateLogin():
    user = validateSession()
    if user:
        return user
    else:
        return make_response({"mensagem" : "Usuário não autenticado."}, 401)
    
def validateSession():
    if "user" in session:
        return session["user"]
    else:
        return None