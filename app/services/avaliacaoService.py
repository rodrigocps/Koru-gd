from sqlite3 import connect, Row, Error
from flask import session
from app.database import DATABASE_PATH
import app.services.utils as utils
import app.exceptions.apiExceptions as exceptions
import app.services.authService as auth

def adicionarAvaliacao(data, empresaId):
    user = auth.validateLogin()
    try:
        with connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()

            query = "INSERT INTO avaliacoes(titulo, texto, empresa_id, autor_id) VALUES (?, ?, ?, ?)"

            cursor.execute(query, (data["titulo"], data["texto"], empresaId, user["id"],))
            
            conn.commit()

            avaliacao = data.copy()
            avaliacao["id"] = cursor.lastrowid

            return avaliacao
    except Error as e:
        conn.rollback()
        print(e)
        return exceptions.throwCreateAvaliacaoException()
    finally:
        conn.close()


def getAvaliacoes(empresaId):
    conn = connect(DATABASE_PATH)
    conn.row_factory = Row

    cursor = conn.cursor()

    query = "SELECT av.id, av.empresa_id, av.titulo, av.texto, u.nome as autor_name, u.email as autor_email FROM avaliacoes av LEFT JOIN usuarios u ON u.id = av.autor_id WHERE av.empresa_id = ?"
    
    cursor.execute(query, (empresaId,))
    rows = cursor.fetchall()

    avaliacoes = utils.row_list_to_dict_list(rows)

    conn.close()

    if "user" in session:
        user = session["user"]
        userAvaliacoes = getUserAvaliacoes(empresaId, user["id"])

        avReturn = []

        for av in avaliacoes:
            for uav in userAvaliacoes:
                if(uav["id"]== av["id"]):
                    av["isClientOwner"] = True
            
            avReturn.append(av)

        return avReturn

    else:
        return avaliacoes

def getAvaliacao(empresaId, avaliacaoId):
    conn = connect("banco.db")
    conn.row_factory = Row

    cursor = conn.cursor()
    query = "SELECT av.id, av.empresa_id, av.titulo, av.texto, u.nome as autor_name, u.email as autor_email FROM avaliacoes av LEFT JOIN usuarios u ON u.id = av.autor_id WHERE av.empresa_id = ? AND av.id = ?"

    cursor.execute(query, (empresaId, avaliacaoId))
    
    avaliacao = cursor.fetchone()
    conn.close()

    if(avaliacao):
        return utils.row_to_dict(avaliacao)
    else:
        return exceptions.throwAvaliacaoNotFoundException()

def excluirAvaliacao(empresaId, avaliacaoId):
    avaliacao = getAvaliacao(empresaId, avaliacaoId)
    user = auth.validateLogin()

    if(user["email"] != avaliacao["autor_email"]):
        return exceptions.throwUnauthorizedDeleteAvaliacaoException();
    
    conn = connect("banco.db")

    cursor = conn.cursor()
    cursor.execute("DELETE FROM avaliacoes WHERE empresa_id = ? and id = ?", (empresaId, avaliacaoId))

    conn.commit()
    conn.close()

    return avaliacao


def editarAvaliacao(empresaId, avaliacaoId, avaliacao):
    savedAvaliacao = getAvaliacao(empresaId, avaliacaoId) # Checar se existe a avaliação no Banco.
    user = auth.validateLogin()
    
    if(user["email"] != savedAvaliacao["autor_email"]):
        return exceptions.throwUnauthorizedUpdateAvaliacaoException();
    
    try:
        with connect(DATABASE_PATH) as conn:
            conn = connect("banco.db")

            cursor = conn.cursor()
            cursor.execute("UPDATE avaliacoes SET titulo = ?, texto = ? WHERE empresa_id = ? AND id = ?", (avaliacao["titulo"], avaliacao["texto"], empresaId, avaliacaoId))

            conn.commit()
            
            return getAvaliacao(empresaId, avaliacaoId)
    except:
        conn.rollback()
        return exceptions.throwUpdateAvaliacaoException()

    finally:
        conn.close() 

def getUserAvaliacoes(empresaId, userId):
    conn = connect(DATABASE_PATH)
    conn.row_factory = Row

    cursor = conn.cursor()

    query = '''
        SELECT av.id, av.empresa_id, av.titulo, av.texto, u.nome as autor_name, u.email as autor_email
        FROM avaliacoes av 
        LEFT JOIN usuarios u 
        ON u.id = av.autor_id 
        WHERE av.empresa_id = ? 
        AND av.autor_id = ?
    '''
    
    cursor.execute(query, (empresaId,userId))
    rows = cursor.fetchall()

    avaliacoes = utils.row_list_to_dict_list(rows)

    conn.close()

    return avaliacoes
