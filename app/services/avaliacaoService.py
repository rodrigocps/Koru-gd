from sqlite3 import connect, Row
from app.database import DATABASE_PATH
import app.services.utils as utils
import app.exceptions.apiExceptions as exceptions

def adicionarAvaliacao(data, empresaId):
    try:
        with connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()

            query = "INSERT INTO avaliacoes(titulo, texto, empresa_id, autor_id) VALUES (?, ?, ?, ?)"
            
            cursor.execute(query, (data["titulo"], data["texto"], empresaId, 1))
            
            conn.commit()

            avaliacao = data.copy()
            avaliacao["id"] = cursor.lastrowid

            return avaliacao
    except:
        conn.rollback()
        return exceptions.throwCreateAvaliacaoException()
    finally:
        conn.close()


def getAvaliacoes(empresaId):
    conn = connect(DATABASE_PATH)
    conn.row_factory = Row

    cursor = conn.cursor()

    query = "SELECT * FROM avaliacoes where empresa_id = ?"
    
    cursor.execute(query, (empresaId,))
    rows = cursor.fetchall()

    avaliacoes = utils.row_list_to_dict_list(rows)

    conn.close()

    return avaliacoes

def getAvaliacao(empresaId, avaliacaoId):
    conn = connect("banco.db")
    conn.row_factory = Row

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM avaliacoes where empresa_id = ? AND id = ?", (empresaId, avaliacaoId))
    
    avaliacao = cursor.fetchone()
    conn.close()

    if(avaliacao):
        return utils.row_to_dict(avaliacao)
    else:
        return exceptions.throwAvaliacaoNotFoundException()

def excluirAvaliacao(empresaId, avaliacaoId):
    avaliacao = getAvaliacao(empresaId, avaliacaoId)
    
    conn = connect("banco.db")

    cursor = conn.cursor()
    cursor.execute("DELETE FROM avaliacoes WHERE empresa_id = ? and id = ?", (empresaId, avaliacaoId))

    conn.commit()
    conn.close()

    return avaliacao


def editarAvaliacao(empresaId, avaliacaoId, avaliacao):
    getAvaliacao(empresaId, avaliacaoId) # Checar se existe a avaliação no Banco.
    
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
