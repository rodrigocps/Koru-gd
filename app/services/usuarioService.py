import sqlite3

def adicionarUsuario(usuario) :
    msg = ""
    try:
        with sqlite3.connect("banco.db") as conn:
            cursor = conn.cursor()
            query = "INSERT INTO usuarios(nome, email, senha) VALUES (?, ?, ?)"

            cursor.execute(query, (usuario["nome"], usuario["email"], usuario["senha"]))
            conn.commit()
            msg = "Usuário adicionado com sucesso."
    except:
        msg = "Erro ao adicionar usuário."
        conn.rollback()
        return False, msg
    finally:
        conn.close()
    return True, msg

def autenticarUsuario(usuario):
    return True

def atualizarUsuario() :
    return True

def removerUsuario() :
    return True