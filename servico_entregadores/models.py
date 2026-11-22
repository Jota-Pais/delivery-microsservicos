from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Entregador(db.Model):
    """Entregador do delivery.

    ativo: o entregador trabalha aqui (cadastro válido).
    disponivel: está livre agora, sem nenhuma entrega em andamento.
    """
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    veiculo = db.Column(db.String(50), nullable=False)
    disponivel = db.Column(db.Boolean, nullable=False, default=True)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def para_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "veiculo": self.veiculo,
            "disponivel": self.disponivel,
            "ativo": self.ativo,
            "criado_em": self.criado_em.isoformat(timespec="seconds"),
        }
