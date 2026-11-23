# Delivery em Microsserviços

> RASCUNHO para revisão do grupo. Pontos marcados com (confirmar) dependem do documento do grupo.

## Propósito do sistema
Sistema de delivery de comida dividido em quatro microsserviços independentes (clientes, cardápio, entregadores e pedidos). Ele permite registrar pedidos garantindo que o cliente e o prato estejam ativos e que haja um entregador livre, cada serviço com o seu próprio banco e se comunicando só por HTTP.

## Usuários
- **Cliente:** faz pedidos de pratos do cardápio.
- **Entregador:** recebe e realiza as entregas.
- **Administrador do restaurante:** mantém o cardápio, os clientes e os entregadores.

## Requisitos funcionais
1. O sistema deve permitir cadastrar, listar, consultar, atualizar e inativar clientes (nome, telefone e endereço).
2. O sistema deve permitir consultar se um cliente está ativo.
3. O sistema deve permitir cadastrar, listar, consultar, atualizar e inativar pratos, com preço maior que zero.
4. O sistema deve permitir consultar um prato com seu preço e se está disponível.
5. O sistema deve permitir cadastrar, listar, consultar, atualizar e inativar entregadores (nome e veículo).
6. O sistema deve permitir marcar um entregador como ocupado e depois liberá-lo, recusando ocupar um entregador inativo ou já ocupado.
7. O sistema deve permitir registrar um pedido (confirmar), somente para cliente ativo, prato ativo e entregador livre.
8. O sistema deve desfazer o pedido caso não seja possível ocupar o entregador.
9. O sistema deve informar uma mensagem clara quando outro serviço estiver indisponível.

## Descritivo técnico

| Microsserviço | Porta | Banco | Função |
|---|---|---|---|
| servico_clientes | 5001 | clientes.db | Cadastro de clientes e consulta "está ativo?" |
| servico_cardapio | 5002 | cardapio.db | Cadastro de pratos e fornecimento de nome, preço e disponibilidade |
| servico_entregadores | 5003 | entregadores.db | Cadastro de entregadores e controle ocupado/livre |
| servico_pedidos | 5004 | pedidos.db | Registro dos pedidos, orquestrando os outros três serviços |

Cada serviço tem seu banco SQLite, seu `requirements.txt` e uma rota `/api/health`. Ao iniciar, cria dados iniciais se o banco estiver vazio.

## Integrações
| # | Tipo | Quem chama | Quem responde | Rota usada | O que faz |
|---|---|---|---|---|---|
| 1 | Busca | pedidos | clientes | GET /api/clientes/<id>/ativo | Confere se o cliente está ativo |
| 2 | Busca | pedidos | cardapio | GET /api/pratos/<id> | Obtém preço e se o prato está ativo |
| 3 | Alteração | pedidos | entregadores | PATCH /api/entregadores/<id>/ocupar | Marca o entregador como ocupado; se devolver 400, o pedido é desfeito |

## Como executar
1. `py -m venv .venv` e `.venv\Scripts\Activate.ps1`
2. `pip install -r requirements.txt`
3. No VS Code: Executar e Depurar > **Iniciar os 4 serviços**
4. Importar `thunder-client-colecao.json` no Thunder Client e os ambientes de `thunder-ambientes/` (Local e Render). Selecionar o ambiente ativo.

## Publicação (Render)
| Serviço | Link |
|---|---|
| servico_clientes | (a preencher) |
| servico_cardapio | (a preencher) |
| servico_entregadores | (a preencher) |
| servico_pedidos | (a preencher) |
