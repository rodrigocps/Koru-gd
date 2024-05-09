from flask import make_response
from sqlite3 import connect, Row
from app.database import DATABASE_PATH
import app.services.utils as utils
import app.exceptions.apiExceptions as exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from app.database import DATABASE_PATH
'''
1- função logout aqui
2 - O que fará atualização de usuário? alterar nome? alterar senha? alterar email?
3-
4- Utilizo a hash aqui ? 
'''

def adicionarUsuario(usuario):
    try:
        with connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email=?", (usuario["email"],))
            if cursor.fetchall()[0] > 0:
                return exceptions.throwUsuarioExistente()  # BAD REQUEST 400
                
            else:
                # Gerar hash da senha
                hashed_password = generate_password_hash(usuario["senha"])

                # Inserir novo usuário
                query = "INSERT INTO usuarios (nome,email,senha) VALUES(?,?,?)"
                cursor.execute(query, (usuario["nome"], usuario["email"], hashed_password))
                conn.commit()            

                return make_response({"mensagem": "Usuário criado com sucesso"}, 201)  # CREATED
                
    except Exception as e:
        print("Erro ao adicionar usuário:", e)
        conn.rollback()
        return exceptions.throwCreateUsuarioException()
    
    finally:
        conn.close()
#PUT recebe a atualização do usuario
def autenticarUsuario(usuario):
    return True

def atualizarUsuario() :
    return True

def removerUsuario() :
    return True

def logoutUsuario():
    return True