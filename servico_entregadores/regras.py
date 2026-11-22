"""Regras de negócio. Aqui ficam as decisões do serviço (sem Flask, sem rotas)."""
from erros import RegraDeNegocioError
from models import Entregador, db

CAMPOS_OBRIGATORIOS = ("nome", "veiculo")


def _validar(dados):
    """Confere os campos obrigatórios e devolve os valores já sem espaços."""
    valores = {}
    for campo in CAMPOS_OBRIGATORIOS:
        valor = str(dados.get(campo) or "").strip()
        if not valor:
            raise RegraDeNegocioError(f"O campo '{campo}' é obrigatório.")
        valores[campo] = valor
    return valores


def criar(dados):
    entregador = Entregador(**_validar(dados))  # disponivel e ativo começam True
    db.session.add(entregador)
    db.session.commit()
    return entregador


def dados_iniciais():
    """Cria os entregadores de exemplo se o banco estiver vazio.

    No Render gratuito o arquivo .db é apagado quando o serviço reinicia ou hiberna;
    por isso o serviço recria os dados de exemplo sempre que acorda.
    Os entregadores 1 e 2 começam ativos e livres.
    """
    if Entregador.query.count() == 0:
        db.session.add(Entregador(nome="Carlos Mendes", veiculo="Moto"))
        db.session.add(Entregador(nome="Daniela Rocha", veiculo="Bicicleta"))
        db.session.commit()


def listar():
    return Entregador.query.order_by(Entregador.id).all()


def buscar(entregador_id):
    return db.session.get(Entregador, entregador_id)


def atualizar(entregador_id, dados):
    entregador = buscar(entregador_id)
    if entregador is None:
        return None
    valores = _validar(dados)
    entregador.nome = valores["nome"]
    entregador.veiculo = valores["veiculo"]
    db.session.commit()
    return entregador


def inativar(entregador_id):
    entregador = buscar(entregador_id)
    if entregador is None:
        return None
    if not entregador.ativo:
        raise RegraDeNegocioError("O entregador já está inativo.")
    entregador.ativo = False
    db.session.commit()
    return entregador


def ocupar(entregador_id):
    """Chamado pelo serviço de PEDIDOS ao criar um pedido.

    Se o entregador já estiver ocupado, recusa com erro (vira 400): é esse 400
    que avisa o pedidos para desfazer o pedido.
    """
    entregador = buscar(entregador_id)
    if entregador is None:
        return None
    if not entregador.ativo:
        raise RegraDeNegocioError("Entregador inativo")
    if not entregador.disponivel:
        raise RegraDeNegocioError("Entregador já está em uma entrega")
    entregador.disponivel = False
    db.session.commit()
    return entregador


def liberar(entregador_id):
    """Faz o contrário do ocupar: o entregador volta a ficar livre."""
    entregador = buscar(entregador_id)
    if entregador is None:
        return None
    entregador.disponivel = True
    db.session.commit()
    return entregador
