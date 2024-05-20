from app import db
from app.models import Avaliacao, Empresa, Usuario
from app.serializer import AvaliacaoSchema, validate
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError, NoResultFound, DatabaseError
import app.exceptions.apiExceptions as exceptions
from app.services import authService as auth
from flask import session

def adicionarAvaliacao(data, empresaId):
    user = auth.validateSession()
    if not user:
        return exceptions.throwUserNotAuthenticatedException()
    
    try:
        a = validate(data, AvaliacaoSchema())

        avaliacao = Avaliacao(
            titulo = a["titulo"],
            texto = a["texto"],
            author_id = user["id"],
            empresa_id = empresaId
        )

        db.session.add(avaliacao)
        db.session.commit()

        return avaliacao.to_dict()
    except IntegrityError:
        return exceptions.throwCreateAvaliacaoException()


def getAvaliacoes(empresaId):
    empresa = db.session.get(Empresa, empresaId)
    if(empresa):
        avaliacoes = db.session.scalars(empresa.avaliacoes.select()).all()

        return [avWthOwner(avaliacao.to_dict()) for avaliacao in avaliacoes]
    else:
        return exceptions.throwEmpresaNotFoundException()
    
def getAllAvaliacoes():
    u = auth.validateSession()
    if not u:
        return exceptions.throwUserNotAuthenticatedException()

    query = sa.select(Avaliacao).where(Avaliacao.author_id == u["id"])
    avaliacoes = db.session.scalars(query).all()

    return [avWthOwner(avaliacao.to_dict_fetch_empresa()) for avaliacao in avaliacoes]

        
def getAvaliacao(empresaId, avaliacaoId):
    empresa = db.session.get(Empresa, empresaId)
    if(empresa):
        try:
            avaliacao = db.session.scalars(sa.select(Avaliacao).where(Avaliacao.id.is_(avaliacaoId))).one()
            return avWthOwner(avaliacao.to_dict())
        except NoResultFound:
            return exceptions.throwAvaliacaoNotFoundException()
    else:
        return exceptions.throwEmpresaNotFoundException()
    
def avWthOwner(avaliacao):
    user = auth.validateSession()
    if("tipo" in user and user["tipo"]== 'ADMIN'):
        avaliacao["isClientAdmin"] = True

    if user and user["email"] == avaliacao["author"]["email"]:
        avaliacao["isClientOwner"] = True

    return avaliacao

def excluirAvaliacao(empresaId, avaliacaoId):
    u = auth.validateSession()
    if not u:
        return exceptions.throwUserNotAuthenticatedException()
    
    usuario = db.session.get(Usuario, u["id"])

    if not usuario:
        session.clear()
        return exceptions.throwUsuárioNotFoundException()

    try:
        query = sa.select(Avaliacao).where(sa.and_(Avaliacao.id == avaliacaoId, Avaliacao.empresa_id == empresaId)).options(sa.orm.joinedload(Avaliacao.author))
        avaliacao = db.session.scalars(query).one()

        if(avaliacao.author_id != usuario.id and usuario.tipo != 'ADMIN'):
            return exceptions.throwUnauthorizedDeleteAvaliacaoException()

        db.session.delete(avaliacao)
        db.session.commit()

        return avaliacao.to_dict()
    except NoResultFound:
        db.session.rollback()
        return exceptions.throwAvaliacaoNotFoundException()
    except DatabaseError as e:
        print(e)
        db.session.rollback()
        return exceptions.throwUpdateAvaliacaoException()



def editarAvaliacao(empresaId, avaliacaoId, data):
    u = auth.validateSession()
    
    if not u:
        return exceptions.throwUserNotAuthenticatedException()
    
    usuario = db.session.get(Usuario, u["id"])
    if not usuario:
        session.clear()
        return exceptions.throwUsuárioNotFoundException()
    
    novaAvaliacao = validate(data, AvaliacaoSchema())

    try:
        avaliacao = db.session.scalars(usuario.avaliacoes.select().where(sa.and_(Avaliacao.id == avaliacaoId, Avaliacao.empresa_id == empresaId))).one()
        
        query = sa.update(Avaliacao).where(Avaliacao.id == avaliacaoId).values(**novaAvaliacao)
        db.session.execute(query)
        db.session.commit()

        return avaliacao.to_dict()
    except NoResultFound:
        db.session.rollback()
        return exceptions.throwAvaliacaoNotFoundException()
    except DatabaseError as e:
        print(e)
        db.session.rollback()
        return exceptions.throwUpdateAvaliacaoException()
