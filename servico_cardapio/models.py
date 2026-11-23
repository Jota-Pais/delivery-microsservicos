from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Prato(db.Model):
    """Prato do cardápio. 'ativo' significa prato disponível para pedido."""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def para_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "ativo": self.ativo,
            "criado_em": self.criado_em.isoformat(timespec="seconds"),
        }
