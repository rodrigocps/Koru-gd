from sqlite3 import connect, Row
from app.database import DATABASE_PATH
import app.services.utils as utils
import app.exceptions.apiExceptions as exceptions

# 1- É aqui que vai uma função ou método para só acessar esses registros caso esteja logado ?

def listarEmpresas(pagina):
    conn = connect("banco.db")
    conn.row_factory = Row

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empresas ORDER BY id LIMIT 20 OFFSET ?", (((pagina-1) * 10),))
    
    empresas = cursor.fetchall()
    conn.close()

    return utils.row_list_to_dict_list(empresas)


def getEmpresa(empresaId):
    conn = connect("banco.db")
    conn.row_factory = Row

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empresas WHERE id = ?", (empresaId,))
    
    empresa = cursor.fetchone()

    conn.close()

    if(empresa):
        return utils.row_to_dict(empresa)
    else:
        return exceptions.throwEmpresaNotFoundException()