from sqlite3 import connect, Row
from app.database import DATABASE_PATH
import app.services.utils as utils
import app.exceptions.apiExceptions as exceptions

# 1- É aqui que vai uma função ou método para só acessar esses registros caso esteja logado ?
# Sim

def listarEmpresas(pagina, search):
    conn = connect(DATABASE_PATH)
    conn.row_factory = Row

    cursor = conn.cursor()

    sql = "SELECT * FROM empresas {} ORDER BY id LIMIT 20 OFFSET ?"

    if search :
        sql = sql.format("""
            WHERE LOWER(nome) LIKE '%' || LOWER(?) || '%' 
            OR LOWER(setor) LIKE '%' || LOWER(?) || '%'
        """)
        cursor.execute(sql, (search, search, ((pagina-1) * 10),))

    else:
        sql = sql.format("")
        cursor.execute(sql, (((pagina-1) * 10),))
    
    empresas = cursor.fetchall()
    conn.close()

    return utils.row_list_to_dict_list(empresas)


def getEmpresa(empresaId):
    conn = connect(DATABASE_PATH)
    conn.row_factory = Row

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empresas WHERE id = ?", (empresaId,))
    
    empresa = cursor.fetchone()

    conn.close()

    if(empresa):
        return utils.row_to_dict(empresa)
    else:
        return exceptions.throwEmpresaNotFoundException()