from app import db
from flask import make_response, jsonify
import sqlalchemy as sa
import app.exceptions.apiExceptions as exceptions
from app.serializer import EmpresaSchema, validate
from app.models import Empresa


def saveEmpresa(data):
    try:
        e = validate(data, EmpresaSchema())
    
        empresa = Empresa(
            nome = e["nome"],
            setor = e["setor"],
            logo_url = e["logo_url"]
        )

        db.session.add(empresa)
        db.session.commit()

        return make_response(empresa.to_dict(), 200)
    
    except:
        print("erro")
        db.session.rollback()
        return make_response({"mensagem" : "Ocorreu um erro ao adicionar empresa."}, 400)
    
    

def listarEmpresas(pagina, search):
    if(search):
        query = sa.select(Empresa).where(sa.or_(
            sa.func.lower(Empresa.nome).like(sa.func.lower('%{}%'.format(search))),
            sa.func.lower(Empresa.setor).like(sa.func.lower('%{}%'.format(search)))
        )).offset(pagina).limit(20)
    else:
        query = sa.select(Empresa).offset(pagina).limit(20)
        
    empresas = db.session.scalars(query).all()

    if(len(empresas) > 0):
        return jsonify(
            {
                "pagina" : pagina,
                "totalPaginas" : getTotalPaginas(search),
                "empresas" : [empresa.to_dict() for empresa in empresas]
            }
        )
    else:
        return {"empresas": []}



def getEmpresa(empresaId):
    empresa = db.session.get(Empresa, empresaId)

    if(empresa):
        return empresa.to_dict()
    else:
        return exceptions.throwEmpresaNotFoundException()

def getTotalPaginas(search):
    total = 1
    if(search):
        query = sa.select(sa.func.count(Empresa.id)).where(sa.or_(
            sa.func.lower(Empresa.nome).like(sa.func.lower('%{}%'.format(search))),
            sa.func.lower(Empresa.setor).like(sa.func.lower('%{}%'.format(search)))
        ))
    else:
        query = sa.select(sa.func.count(Empresa.id))

    total = db.session.execute(query).scalar()

    if(total == 0):
        return 0

    if(total < 20 and total>0):
        return 1
    
    totalPaginas = total // 20
    
    return totalPaginas
