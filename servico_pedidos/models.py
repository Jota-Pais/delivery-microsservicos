from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Pedido(db.Model):
    """Pedido de delivery.

    cliente_id, prato_id e entregador_id são só números (sem ForeignKey):
    clientes, pratos e entregadores ficam em OUTROS serviços, com OUTROS bancos.
    """
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, nullable=False)
    prato_id = db.Column(db.Integer, nullable=False)
    entregador_id = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Float, nullable=False)  # preço do prato no momento do pedido
    status = db.Column(db.String(20), nullable=False, default="confirmado")  # confirmado ou cancelado
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def para_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "prato_id": self.prato_id,
            "entregador_id": self.entregador_id,
            "valor": self.valor,
            "status": self.status,
            "criado_em": self.criado_em.isoformat(timespec="seconds"),
        }
