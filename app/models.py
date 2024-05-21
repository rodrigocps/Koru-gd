from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from datetime import datetime, timezone
from werkzeug.security import check_password_hash, generate_password_hash


class Usuario(db.Model):
    __tablename__ = "usuarios"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    nome: so.Mapped[str] = so.mapped_column(sa.String(120))
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    senha: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    tipo: so.Mapped[str] = so.mapped_column(sa.String(5), index=True, default="USER", unique=False)

    avaliacoes: so.WriteOnlyMapped['Avaliacao'] = so.relationship(back_populates='author')

    def __repr__(self):
        return '<User {}>'.format(self.email)
    
    def set_password(self, senha):
        self.senha = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.senha, senha)
    
    def to_dict(self):
        return {"id":self.id, "nome":self.nome, "email":self.email, "tipo": self.tipo}
    
    def to_dict_fetch_avaliacoes(self):
        avaliacoes = db.session.scalars(
            sa.select(Avaliacao).where(Avaliacao.author_id == self.id)
        ).all()

        return {
            "id":self.id, 
            "nome":self.nome, 
            "email":self.email, 
            "tipo": self.tipo,
            "avaliacoes": [avaliacao.to_dict() for avaliacao in avaliacoes]
        }
    
    
class Empresa(db.Model):
    __tablename__ = "empresas"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    nome: so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
    setor: so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
    logo_url: so.Mapped[str] = so.mapped_column(sa.Text())

    avaliacoes: so.WriteOnlyMapped['Avaliacao'] = so.relationship(back_populates='empresa')

    def __repr__(self):
        return '<Empresa {}: {}>'.format(self.id, self.nome)
    
    def to_dict(self):
        return {
            "id" : self.id,
            "nome": self.nome,
            "setor" : self.setor,
            "logo_url" : self.logo_url
        }
                
    
class Avaliacao(db.Model):
    __tablename__ = "avaliacoes"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    titulo: so.Mapped[str] = so.mapped_column(sa.String(100))
    texto: so.Mapped[str] = so.mapped_column(sa.Text())
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    
    author_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Usuario.id), index=True)
    empresa_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Empresa.id), index=True)

    author: so.Mapped['Usuario'] = so.relationship(back_populates='avaliacoes')
    empresa: so.Mapped['Empresa'] = so.relationship(back_populates='avaliacoes')

    def __repr__(self):
        return '<Avaliacao {}: {}. "{}">'.format(self.id, self.titulo, self.autor)
    
    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "texto" : self.texto,
            "author": {
                "email": self.author.email,
                "nome" : self.author.nome
            },
            "empresa_id" : self.empresa_id
        }
    
    def to_dict_fetch_empresa(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "texto" : self.texto,
            "author": {
                "email": self.author.email,
                "nome" : self.author.nome
            },
            "empresa" : self.empresa.to_dict()
        }