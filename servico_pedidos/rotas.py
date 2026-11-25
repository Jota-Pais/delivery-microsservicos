from flask import Blueprint, jsonify, request

import regras

rotas = Blueprint("pedidos", __name__, url_prefix="/api")


def _nao_encontrado():
    return jsonify(erro="Pedido não encontrado."), 404


# Cria o pedido: aqui acontecem as 3 integrações (ver regras.py).
@rotas.post("/pedidos")
def criar():
    pedido = regras.criar(request.get_json(silent=True) or {})
    return jsonify(pedido.para_dict()), 201


@rotas.get("/pedidos")
def listar():
    return jsonify([p.para_dict() for p in regras.listar()])


@rotas.get("/pedidos/<int:pedido_id>")
def buscar(pedido_id):
    pedido = regras.buscar(pedido_id)
    return jsonify(pedido.para_dict()) if pedido else _nao_encontrado()


# Cancela o pedido e libera o entregador.
@rotas.patch("/pedidos/<int:pedido_id>/cancelar")
def cancelar(pedido_id):
    pedido = regras.cancelar(pedido_id)
    return jsonify(pedido.para_dict()) if pedido else _nao_encontrado()
