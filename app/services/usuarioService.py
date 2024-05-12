from flask import make_response,request
from sqlite3 import connect
from app.database import DATABASE_PATH
import app.services.utils as utils
import app.exceptions.apiExceptions as exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from app.database import DATABASE_PATH
import sqlite3

def adicionarUsuario(usuario):
    session.clear()
    try:
        with connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email=?", (usuario["email"],))
            row = cursor.fetchone()

            if row[0] == 0:
                hashed_password = generate_password_hash(usuario["senha"])

                # Inserir novo usuário
                query = "INSERT INTO usuarios (nome,email,senha) VALUES(?,?,?)"
                cursor.execute(query, (usuario["nome"], usuario["email"], hashed_password))
                conn.commit()                

                # Logar novo usuário
                cursor.execute("SELECT * FROM usuarios WHERE email = ?", (usuario["email"],))
                new_user = cursor.fetchone()
                if new_user:
                    session["user"] = {"id":row[0], "nome":row[1], "email":row[2]}
                    print(session)
                return make_response({"mensagem": "Usuário criado com sucesso"}, 201)  # CREATED
            else:
                return exceptions.throwUsuarioExistente()
                            
    except sqlite3.Error as e:
        print("Erro ao adicionar usuário:", e)
        conn.rollback()
        return exceptions.throwCreateUsuarioException()    
    finally:
        conn.close()


def getUsuario(id):
    return ""

def login(usuario):
    session.clear()
    try:
        with connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM usuarios WHERE email = ?", (usuario["email"],))
            row = cursor.fetchone()

            if row is None or not check_password_hash(row[3], usuario["senha"]):
                return make_response({"mensagem": "Usuário / senha incorreta."}, 401) # UNAUTHORIZED/UNAUTHENTICATED

            session["user"] = {"id":row[0], "nome":row[1], "email":row[2]}
            print(session)
            return make_response({"mensagem": "Usuário logado com sucesso"}, 200)  # CREATED
    except sqlite3.Error as e:
        print("Erro ao logar o usuário:", e)
        if conn.in_transaction:
            conn.rollback()
        return exceptions.throwUsuárioNotFoundException()
    finally:
        conn.close()



def logout():
    session.clear()
    return {"mensagem" : "Usuário deslogado"}

def atualizarUsuario() :
    return True

def removerUsuario() :
    return True
