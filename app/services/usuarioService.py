from flask import make_response
from sqlite3 import connect, Row
from app.database import DATABASE_PATH
import app.services.utils as utils
import app.exceptions.apiExceptions as exceptions

def adicionarUsuario(usuario) :
    try:
        with connect("banco.db") as conn:
            cursor = conn.cursor()
            query = "INSERT INTO usuarios(nome, email, senha) VALUES (?, ?, ?)"

            cursor.execute(query, (usuario["nome"], usuario["email"], usuario["senha"]))
            conn.commit()

            return make_response({"mensagem" : "Usuário criado com sucesso"}, 201) #CREATED
    except:
        conn.rollback()
        return exceptions.throwCreateUsuarioException()
    finally:
        conn.close()

def autenticarUsuario(usuario):
    return True

def atualizarUsuario() :
    return True

def removerUsuario() :
    return True