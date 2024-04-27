import sqlite3
import json

conn = sqlite3.connect("banco.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    senha TEXT NOT NULL
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS empresas (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    setor TEXT
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS avaliacoes (
    id INTEGER PRIMARY KEY,
    titulo TEXT NOT NULL,
    texto TEXT NOT NULL,
    autor_id INTEGER NOT NULL,
    empresa_id INTEGER NOT NULL,
    FOREIGN KEY (autor_id) REFERENCES usuarios(id),
    FOREIGN KEY (empresa_id) REFERENCES empresas(id)
)
""")

conn.close()

conn = sqlite3.connect("banco.db")
empresas = json.load(open("./app/static/resources/1100_empresas.json", encoding="utf8"))
# empresas_ordenadas = sorted(empresas, key=lambda x: x['nome'])

for empresa in empresas:
    try:
        cursor = conn.cursor()
        query = "INSERT INTO empresas(nome, setor) VALUES(?,?)"
        cursor.execute(query, (empresa["nome"], empresa["setor"]))
        conn.commit()
    except:
        conn.rollback()

conn.close()

