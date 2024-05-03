import sqlite3

def adicionarAvaliacao(avaliacao, empresaId):
    msg = ""
    try:
        with sqlite3.connect("banco.db") as conn:
            cursor = conn.cursor()
            query = "INSERT INTO avaliacoes(titulo, texto, empresa_id, autor_id) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (avaliacao["titulo"], avaliacao["texto"], empresaId, 1))
            conn.commit()
            msg = "Avaliação adicionada com sucesso."
            return True, msg
    except:
        msg= "Erro ao adicionar avaliação."
        conn.rollback()
        return False, msg
    
    finally:
        conn.close()


def getAvaliacoes(empresaId):
    conn = sqlite3.connect("banco.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM avaliacoes where empresa_id = {}".format(empresaId))
    
    avaliacoes = cursor.fetchall()
    conn.close()

    return avaliacoes