from flask import make_response, jsonify
from app.serializer import UsuarioSchema, UsuarioLoginSchema
from app.models import Usuario
import sqlalchemy as sa
from sqlalchemy.exc import NoResultFound, IntegrityError
from app import db
from flask import session
import app.exceptions.apiExceptions as exceptions

def adicionarUsuario(data):
    session.clear()

    try:
        u = UsuarioSchema().load(data)

        usuario = Usuario(nome=u["nome"], email=u["email"])
        usuario.set_password(u["senha"])

        db.session.add(usuario)
        db.session.commit()

        session["user"] = usuario.to_dict()

        return make_response(session["user"], 201)
    except IntegrityError as e:
        db.session.rollback()
        return make_response({"mensagem":"Já existe um usuário cadastrado com esse email."}, 401)
    except:
        return make_response({"mensagem":"Erro ao cadastrar usuario"}, 400)


def login(data):
    session.clear()

    try:
        u = UsuarioLoginSchema().load(data)

        query = sa.select(Usuario).where(Usuario.email.like(u["email"]))

        usuario = db.session.scalars(query).one()

        session["user"] = usuario.to_dict()

        return make_response(session["user"], 200)
    
    except NoResultFound:
        return exceptions.throwUsuárioNotFoundException()


# def getUsuario(id):
#     return ""

def logout():
    session.clear()
    return {"mensagem" : "Usuário deslogado"}

# def atualizarUsuario() :
#     return True

# def removerUsuario() :
#     return True
