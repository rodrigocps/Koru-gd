from sqlite3 import connect, Row
from app.database import DATABASE_PATH
import app.services.utils as utils

def adicionarUsuario(usuario) :
    try:
        with connect("banco.db") as conn:
            cursor = conn.cursor()
            query = "INSERT INTO usuarios(nome, email, senha) VALUES (?, ?, ?)"

            cursor.execute(query, (usuario["nome"], usuario["email"], usuario["senha"]))
            conn.commit()

            return {"aviso" : "Usuário cadastrado com sucesso."}
    except:
        conn.rollback()
        return {"erro" : "Erro ao cadastrar usuário."}
    finally:
        conn.close()

def autenticarUsuario(usuario):
    return True

def atualizarUsuario() :
    return True

def removerUsuario() :
    return True