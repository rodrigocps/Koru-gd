import os
import sqlalchemy as sa
from app import app, db
from sqlalchemy.exc import DatabaseError, NoResultFound
from app.models import Usuario

app.app_context().push()

basedir = os.path.abspath(os.path.dirname(__file__))

email = os.environ.get("ADMIN_EMAIL")
senha = os.environ.get("ADMIN_SENHA")

# ################ TESTS ONLY ################
# email = "koru@mail.com"
# senha = "koru123"
# ############################################

def addAdmin(email, senha):
    print("=> Configurando usuário administrador...")
    try:
        admin = Usuario(nome="Admin", email=email, tipo="ADMIN")
        admin.set_password(senha)

        db.session.add(admin)
        db.session.commit()
    except DatabaseError as de:
        print("=> Ocorreu um erro ao configurar o administrador.")
        


if(email and senha):
    try:
        query = sa.select(Usuario).where(Usuario.email == email)
        usuario = db.session.scalars(query).one()

        # db.session.execute(sa.delete(Usuario).where(Usuario.id == usuario.id))
        # db.session.commit()
    except NoResultFound as nrf:
        addAdmin(email, senha)
