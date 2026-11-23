from flask import Blueprint, jsonify, request

import regras

rotas = Blueprint("pratos", __name__, url_prefix="/api")


def _nao_encontrado():
    return jsonify(erro="Prato não encontrado."), 404


@rotas.post("/pratos")
def criar():
    prato = regras.criar(request.get_json(silent=True) or {})
    return jsonify(prato.para_dict()), 201


@rotas.get("/pratos")
def listar():
    return jsonify([p.para_dict() for p in regras.listar()])


# Devolve o prato inteiro (com preco e ativo): é a rota que o pedidos consulta.
@rotas.get("/pratos/<int:prato_id>")
def buscar(prato_id):
    prato = regras.buscar(prato_id)
    return jsonify(prato.para_dict()) if prato else _nao_encontrado()


@rotas.put("/pratos/<int:prato_id>")
def atualizar(prato_id):
    prato = regras.atualizar(prato_id, request.get_json(silent=True) or {})
    return jsonify(prato.para_dict()) if prato else _nao_encontrado()


@rotas.patch("/pratos/<int:prato_id>/inativar")
def inativar(prato_id):
    prato = regras.inativar(prato_id)
    return jsonify(prato.para_dict()) if prato else _nao_encontrado()
