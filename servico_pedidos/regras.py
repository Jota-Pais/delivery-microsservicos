"""Regras de negócio do serviço de pedidos (sem Flask, sem rotas).

Para criar um pedido, este serviço "liga" para os outros três:
  1. Busca     -> CLIENTES:     GET   /api/clientes/<id>/ativo
  2. Busca     -> CARDAPIO:     GET   /api/pratos/<id>
  3. Alteração -> ENTREGADORES: PATCH /api/entregadores/<id>/ocupar
"""
import integracao
from erros import RegraDeNegocioError
from models import Pedido, db


def _id_inteiro(dados, campo):
    valor = dados.get(campo)
    if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
        raise RegraDeNegocioError(f"O campo '{campo}' é obrigatório e deve ser um número inteiro.")
    return valor


def _motivo(resposta):
    """Pega a mensagem de erro que o outro serviço mandou."""
    try:
        return resposta.json().get("erro", f"erro {resposta.status_code}")
    except ValueError:
        return f"erro {resposta.status_code}"


def _cliente_ativo(cliente_id):
    print(f"[PEDIDOS] passo 1: pergunto ao CLIENTES se o cliente {cliente_id} está ativo", flush=True)
    resposta = integracao.chamar("CLIENTES", "GET", f"/api/clientes/{cliente_id}/ativo")
    if resposta.status_code == 404:
        raise RegraDeNegocioError("Cliente não encontrado.")
    if not resposta.ok:
        raise RegraDeNegocioError(f"Clientes recusou: {_motivo(resposta)}")
    if not resposta.json()["ativo"]:
        raise RegraDeNegocioError("Cliente inativo.")


def _preco_do_prato(prato_id):
    print(f"[PEDIDOS] passo 2: pergunto ao CARDAPIO o preço do prato {prato_id}", flush=True)
    resposta = integracao.chamar("CARDAPIO", "GET", f"/api/pratos/{prato_id}")
    if resposta.status_code == 404:
        raise RegraDeNegocioError("Prato não encontrado.")
    if not resposta.ok:
        raise RegraDeNegocioError(f"Cardápio recusou: {_motivo(resposta)}")
    prato = resposta.json()
    if not prato["ativo"]:
        raise RegraDeNegocioError("Prato indisponível.")
    return prato["preco"]


def _ocupar_entregador(entregador_id):
    resposta = integracao.chamar("ENTREGADORES", "PATCH", f"/api/entregadores/{entregador_id}/ocupar")
    if resposta.status_code == 404:
        raise RegraDeNegocioError("Entregador não encontrado.")
    if not resposta.ok:
        raise RegraDeNegocioError(f"Entregadores recusou: {_motivo(resposta)}")


def criar(dados):
    cliente_id = _id_inteiro(dados, "cliente_id")
    prato_id = _id_inteiro(dados, "prato_id")
    entregador_id = _id_inteiro(dados, "entregador_id")

    _cliente_ativo(cliente_id)
    preco = _preco_do_prato(prato_id)

    print("[PEDIDOS] passo 3: gravo o pedido no MEU banco (pedidos.db)", flush=True)
    pedido = Pedido(cliente_id=cliente_id, prato_id=prato_id,
                    entregador_id=entregador_id, valor=preco)
    db.session.add(pedido)
    db.session.commit()

    print(f"[PEDIDOS] passo 4: peço ao ENTREGADORES para ocupar o entregador {entregador_id}", flush=True)
    try:
        _ocupar_entregador(entregador_id)
    except RegraDeNegocioError:
        # Cada serviço tem seu banco: não existe "desfazer tudo" automático.
        # Se o entregador não foi ocupado, apagamos o pedido (compensação).
        print("[PEDIDOS] deu errado: apago o pedido gravado (compensação)", flush=True)
        db.session.delete(pedido)
        db.session.commit()
        raise

    print("[PEDIDOS] pronto: pedido confirmado", flush=True)
    return pedido


def dados_iniciais():
    """O pedidos NÃO cria dados iniciais.

    Um pedido só existe depois de conversar com clientes, cardápio e entregadores;
    criar um pedido "de exemplo" sem essas chamadas deixaria os dados incoerentes
    (por exemplo, um entregador ocupado sem saber). Os outros três serviços já
    recriam os seus dados ao ligar, então basta fazer um POST /api/pedidos.
    """


def listar():
    return Pedido.query.order_by(Pedido.id).all()


def buscar(pedido_id):
    return db.session.get(Pedido, pedido_id)


def cancelar(pedido_id):
    pedido = buscar(pedido_id)
    if pedido is None:
        return None
    if pedido.status == "cancelado":
        raise RegraDeNegocioError("O pedido já está cancelado.")
    print(f"[PEDIDOS] cancelando: peço ao ENTREGADORES para liberar o entregador {pedido.entregador_id}", flush=True)
    resposta = integracao.chamar("ENTREGADORES", "PATCH", f"/api/entregadores/{pedido.entregador_id}/liberar")
    if not resposta.ok and resposta.status_code != 404:
        raise RegraDeNegocioError(f"Entregadores recusou: {_motivo(resposta)}")
    pedido.status = "cancelado"
    db.session.commit()
    return pedido
