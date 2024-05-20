from flask import make_response, jsonify
from app.serializer import UsuarioSchema, UsuarioLoginSchema, validate
from app.models import Usuario
from app.services import authService as auth
import sqlalchemy as sa
from sqlalchemy.exc import NoResultFound, IntegrityError
from app import db
from flask import session
import app.exceptions.apiExceptions as exceptions

def adicionarUsuario(data):
    session.clear()

    try:
        u = validate(data, UsuarioSchema())

        usuario = Usuario(nome=u["nome"], email=u["email"])
        usuario.set_password(u["senha"])

        db.session.add(usuario)
        db.session.commit()

        session["user"] = usuario.to_dict()

        return make_response(session["user"], 201)
    except IntegrityError as e:
        db.session.rollback()
        print(e)
        return make_response({"mensagem":"Já existe um usuário cadastrado com esse email."}, 401)
    except:
        return make_response({"mensagem":"Erro ao cadastrar usuario"}, 400)


def login(data):
    session.clear()

    try:
        u = validate(data, UsuarioLoginSchema())

        query = sa.select(Usuario).where(Usuario.email == u["email"])

        usuario = db.session.scalars(query).one()

        session["user"] = usuario.to_dict()
        if not usuario.tipo:
            session["user"]["tipo"] = "USER"

        return make_response(session["user"], 200)
    
    except NoResultFound:
        return exceptions.throwUsuárioNotFoundException()


def getUsuario(id):
    u = auth.validateSession()
    if not u:
        return exceptions.throwUserNotAuthenticatedException()
    
    userId = u["id"]
    if(id and u["tipo"]=='ADMIN'):
        userId = id
    
    try:
        query = sa.select(Usuario).where(Usuario.id == userId)
        usuario = db.session.scalars(query).one()

        return usuario.to_dict()
    except NoResultFound:
        session.clear()
        return exceptions.throwNotFoundException("Usuário não encontrado.")

def logout():
    session.clear()
    return {"mensagem" : "Usuário deslogado"}

def atualizarUsuario(userId, data) :
    sessionUser = auth.validateSession()
    if not sessionUser:
        return exceptions.throwUserNotAuthenticatedException()
    if sessionUser["id"] != userId:
        return exceptions.throwUnauthorizedUpdateException("Somente o próprio usuário pode atualizar sua conta.")
    
    saved = db.session.scalars(sa.select(Usuario).where(Usuario.id == userId)).one()
    if not saved:
        return exceptions.throwUsuárioNotFoundException()
    if not saved.tipo:
        data["tipo"] = "USER"
    try:
        novoUsuario = validate(data, UsuarioSchema())

        query = sa.update(Usuario).where(Usuario.id == userId).values(**novoUsuario)
        db.session.execute(query)
        db.session.commit()

        session["user"] = getUsuario(userId)

        return make_response(session["user"], 201)
    except IntegrityError as e:
        db.session.rollback()
        print(e)
        return make_response({"mensagem":"Já existe um usuário cadastrado com esse email."}, 401)
    except:
        db.session.rollback()
        return make_response({"mensagem":"Erro ao atualizar usuario"}, 400)

# def removerUsuario() :
#     return True
