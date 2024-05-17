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
    if user and user["email"] == avaliacao["author"]["email"]:
        avaliacao["isClientOwner"] = True
        return avaliacao
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
        avaliacao = db.session.scalars(usuario.avaliacoes.select().where(sa.and_(Avaliacao.id.is_(avaliacaoId), Avaliacao.empresa_id.is_(empresaId)))).one()

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
        avaliacao = db.session.scalars(usuario.avaliacoes.select().where(sa.and_(Avaliacao.id.is_(avaliacaoId), Avaliacao.empresa_id.is_(empresaId)))).one()
        
        query = sa.update(Avaliacao).where(Avaliacao.id).values(**novaAvaliacao)
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


# def getUserAvaliacoes(empresaId, userId):
#     conn = get_con()
#     conn.row_factory = Row

#     cursor = conn.cursor()

#     query = '''
#         SELECT av.id, av.empresa_id, av.titulo, av.texto, u.nome as autor_name, u.email as autor_email
#         FROM avaliacoes av 
#         LEFT JOIN usuarios u 
#         ON u.id = av.autor_id 
#         WHERE av.empresa_id = ? 
#         AND av.autor_id = ?
#     '''
    
#     cursor.execute(query, (empresaId,userId))
#     rows = cursor.fetchall()

#     avaliacoes = utils.row_list_to_dict_list(rows)

#     conn.close()

#     return avaliacoes

# def getUserAvaliacao(empresaId, avaliacaoId, userId):
#     conn = get_con()
#     conn.row_factory = Row

#     cursor = conn.cursor()

#     query = '''
#         SELECT av.id, av.empresa_id, av.titulo, av.texto, u.nome as autor_name, u.email as autor_email
#         FROM avaliacoes av 
#         LEFT JOIN usuarios u 
#         ON u.id = av.autor_id 
#         WHERE av.id = ? 
#         AND av.autor_id = ?
#         AND av.empresa_id = ? 
#     '''
    
#     cursor.execute(query, (avaliacaoId,userId, empresaId))
    
#     row = cursor.fetchone()
    
#     conn.close()

#     return utils.row_to_dict(row)

