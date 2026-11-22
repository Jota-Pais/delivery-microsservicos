"""Regras de negócio. Aqui ficam as decisões do serviço (sem Flask, sem rotas)."""
from erros import RegraDeNegocioError
from models import Cliente, db

CAMPOS_OBRIGATORIOS = ("nome", "telefone", "endereco")


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
    cliente = Cliente(**_validar(dados))
    db.session.add(cliente)
    db.session.commit()
    return cliente


def dados_iniciais():
    """Cria os clientes de exemplo se o banco estiver vazio.

    No Render gratuito o arquivo .db é apagado quando o serviço reinicia ou hiberna;
    por isso o serviço recria os dados de exemplo sempre que acorda.
    O cliente 1 fica ativo e o cliente 2 já nasce inativo, para testar o pedidos.
    """
    if Cliente.query.count() == 0:
        db.session.add(Cliente(nome="Ana Souza", telefone="(11) 98888-1111",
                               endereco="Rua das Flores, 100"))
        db.session.add(Cliente(nome="Bruno Lima", telefone="(11) 97777-2222",
                               endereco="Av. Brasil, 2000", ativo=False))
        db.session.commit()


def listar():
    return Cliente.query.order_by(Cliente.id).all()


def buscar(cliente_id):
    return db.session.get(Cliente, cliente_id)


def atualizar(cliente_id, dados):
    cliente = buscar(cliente_id)
    if cliente is None:
        return None
    valores = _validar(dados)
    cliente.nome = valores["nome"]
    cliente.telefone = valores["telefone"]
    cliente.endereco = valores["endereco"]
    db.session.commit()
    return cliente


def inativar(cliente_id):
    cliente = buscar(cliente_id)
    if cliente is None:
        return None
    if not cliente.ativo:
        raise RegraDeNegocioError("O cliente já está inativo.")
    cliente.ativo = False
    db.session.commit()
    return cliente
