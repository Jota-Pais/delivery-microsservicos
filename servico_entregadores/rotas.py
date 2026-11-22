from flask import Blueprint, jsonify, request

import regras

rotas = Blueprint("entregadores", __name__, url_prefix="/api")


def _nao_encontrado():
    return jsonify(erro="Entregador não encontrado."), 404


@rotas.post("/entregadores")
def criar():
    entregador = regras.criar(request.get_json(silent=True) or {})
    return jsonify(entregador.para_dict()), 201


@rotas.get("/entregadores")
def listar():
    return jsonify([e.para_dict() for e in regras.listar()])


@rotas.get("/entregadores/<int:entregador_id>")
def buscar(entregador_id):
    entregador = regras.buscar(entregador_id)
    return jsonify(entregador.para_dict()) if entregador else _nao_encontrado()


@rotas.put("/entregadores/<int:entregador_id>")
def atualizar(entregador_id):
    entregador = regras.atualizar(entregador_id, request.get_json(silent=True) or {})
    return jsonify(entregador.para_dict()) if entregador else _nao_encontrado()


@rotas.patch("/entregadores/<int:entregador_id>/inativar")
def inativar(entregador_id):
    entregador = regras.inativar(entregador_id)
    return jsonify(entregador.para_dict()) if entregador else _nao_encontrado()


# Rotas que o serviço de PEDIDOS usa: ocupar ao criar o pedido, liberar ao terminar/cancelar.
@rotas.patch("/entregadores/<int:entregador_id>/ocupar")
def ocupar(entregador_id):
    entregador = regras.ocupar(entregador_id)
    return jsonify(entregador.para_dict()) if entregador else _nao_encontrado()


@rotas.patch("/entregadores/<int:entregador_id>/liberar")
def liberar(entregador_id):
    entregador = regras.liberar(entregador_id)
    return jsonify(entregador.para_dict()) if entregador else _nao_encontrado()


@rotas.get("/entregadores/<int:entregador_id>/ativo")
def esta_ativo(entregador_id):
    entregador = regras.buscar(entregador_id)
    if entregador is None:
        return _nao_encontrado()
    return jsonify(id=entregador.id, ativo=entregador.ativo)
