import sqlite3

def listarEmpresas(pagina):
    conn = sqlite3.connect("banco.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empresas ORDER BY id LIMIT 10 OFFSET {};".format(((pagina-1) * 10)))
    
    empresas = cursor.fetchall()
    conn.close()

    return empresas


def getEmpresa(empresaId):
    conn = sqlite3.connect("banco.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empresas WHERE id = {}".format(empresaId))
    empresa = cursor.fetchone()
    conn.close()

    return empresa