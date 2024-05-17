import json
from app.save_empresas import get_con, PRODUCAO
def buildTables():
    try:
        conn = get_con()

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS empresas (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            setor TEXT,
            logo_url TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id SERIAL PRIMARY KEY,
            titulo TEXT NOT NULL,
            texto TEXT NOT NULL,
            autor_id INTEGER NOT NULL,
            empresa_id INTEGER NOT NULL,
            FOREIGN KEY (autor_id) REFERENCES usuarios(id),
            FOREIGN KEY (empresa_id) REFERENCES empresas(id)
        )
        """)

        conn.commit()  # Confirmar a transação

        print("Tabelas criadas com sucesso.")
    except Exception as e:
        print("Erro ao criar tabelas:", e)
    finally:
        if conn is not None:
            conn.close()

def addEmpresas():
    conn = get_con()
    empresas = json.load(open("./app/static/resources/1100_empresas.json", encoding="utf8"))
    # empresas_ordenadas = sorted(empresas, key=lambda x: x['nome'])

    for empresa in empresas:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO empresas(nome, setor, logo_url) VALUES(?,?,?)"
            if(PRODUCAO):
                query = query.replace("?", "%s")
            cursor.execute(query, (empresa["nome"], empresa["setor"], empresa["logoUrl"]))
            conn.commit()
        except:
            conn.rollback()

    conn.close()

def checkIfEmpresasTableIsEmpty():
    conn = get_con()

    cursor = conn.cursor()

    query = "SELECT COUNT(*) AS quantidade_empresas FROM empresas"
    
    cursor.execute(query)
    row = cursor.fetchone()

    conn.close()

    if(row[0] > 0):
        return False
    else: 
        return True

def buildDb():
    print("=> Construindo BD (Se não existir)...")
    buildTables()

    if checkIfEmpresasTableIsEmpty():
        print("=> Adicionando empresas...")
        addEmpresas()

    # conn = get_con()
    # cursor = conn.cursor()
    # cursor.execute("""SELECT table_name FROM information_schema.tables
    #     WHERE table_schema = 'public'""")

    # # Exibir o nome de todas as tabelas
    # print("=" * 150)
    # for table in cursor.fetchall():
    #     print(table)
    # print("=" * 150)


    # cursor.close()
    # conn.close()


