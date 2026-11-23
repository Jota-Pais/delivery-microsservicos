"""Regras de negócio. Aqui ficam as decisões do serviço (sem Flask, sem rotas)."""
from erros import RegraDeNegocioError
from models import Prato, db


def _validar(dados):
    nome = (dados.get("nome") or "").strip()
    if not nome:
        raise RegraDeNegocioError("O campo 'nome' é obrigatório.")
    try:
        preco = float(dados.get("preco"))
    except (TypeError, ValueError):
        raise RegraDeNegocioError("O campo 'preco' é obrigatório e deve ser um número.")
    if preco <= 0:
        raise RegraDeNegocioError("O 'preco' deve ser maior que zero.")
    return nome, preco


def criar(dados):
    nome, preco = _validar(dados)
    prato = Prato(nome=nome, preco=preco)
    db.session.add(prato)
    db.session.commit()
    return prato


def dados_iniciais():
    """Cria pratos de exemplo se o banco estiver vazio.

    No Render gratuito o arquivo .db é apagado quando o serviço reinicia ou hiberna;
    por isso o serviço recria os dados de exemplo sempre que acorda.
    """
    if Prato.query.count() == 0:
        db.session.add(Prato(nome="X-Burger", preco=25.90, ativo=True))
        db.session.add(Prato(nome="Pizza Calabresa", preco=39.90, ativo=False))
        db.session.commit()


def listar():
    return Prato.query.order_by(Prato.id).all()


def buscar(prato_id):
    return db.session.get(Prato, prato_id)


def atualizar(prato_id, dados):
    prato = buscar(prato_id)
    if prato is None:
        return None
    nome, preco = _validar(dados)
    prato.nome = nome
    prato.preco = preco
    db.session.commit()
    return prato


def inativar(prato_id):
    prato = buscar(prato_id)
    if prato is None:
        return None
    if not prato.ativo:
        raise RegraDeNegocioError("O prato já está inativo.")
    prato.ativo = False
    db.session.commit()
    return prato
