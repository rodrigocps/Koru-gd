from flask import jsonify
from app.services.empresaService import saveEmpresa
import json
from app import app, db, models
import sqlalchemy as sa
from sqlalchemy.exc import DatabaseError

app.app_context().push()

try:
    saved = db.session.scalars(sa.select(models.Empresa)).all()
    if(len(saved) == 0):
        print(" => Copiando empresas para o Banco de dados...")
        empresas = json.load(open("./app/static/resources/1100_empresas.json", encoding="utf8"))

        for i in range(len(empresas)):
            empresa = empresas[i]
            print("--- Copiando empresa... ({}/{})".format((i+1), len(empresas)))
            saveEmpresa({"nome" : empresa["nome"], "setor" : empresa["setor"], "logo_url": empresa["logoUrl"]})
except DatabaseError as e:
    print("Erro ao copiar empresas para o banco de dados.")