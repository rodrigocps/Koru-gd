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

def getAvaliacao(empresaId, avaliacaoId):
    conn = sqlite3.connect("banco.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM avaliacoes where empresa_id = {} AND id = {}".format(empresaId, avaliacaoId))
    
    avaliacao = cursor.fetchone()
    conn.close()

    return avaliacao

def excluirAvaliacao(empresaId, avaliacaoId):
    conn = sqlite3.connect("banco.db")

    cursor = conn.cursor()
    cursor.execute("DELETE FROM avaliacoes WHERE empresa_id = ? and id = ?", (empresaId, avaliacaoId))

    conn.commit()
    conn.close()

def editarAvaliacao(empresaId, avaliacao):
    conn = sqlite3.connect("banco.db")

    cursor = conn.cursor()
    cursor.execute("UPDATE avaliacoes SET titulo = ?, texto = ? WHERE empresa_id = ? AND id = ?", (avaliacao["titulo"], avaliacao["texto"], empresaId, avaliacao["id"]))

    conn.commit()
    conn.close()