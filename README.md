# Nome do projeto

> Este arquivo é o **documento de requisitos** do projeto. Apague as instruções entre `>` e preencha.

## Propósito do sistema
> Em 2 ou 3 frases: que problema o sistema resolve?

## Usuários
> Quem usa o sistema? (ex.: síndico, morador)

## Requisitos funcionais
> Lista curta e numerada, no formato "O sistema deve permitir...".
1. O sistema deve permitir ...
2. O sistema deve permitir ...

## Descritivo técnico

| Microsserviço | Porta | Banco | Função |
|---|---|---|---|
| servico_clientes | 5001 | clientes.db | ... |
| servico_cardapio | 5002 | cardapio.db | ... |
| servico_entregadores | 5003 | entregadores.db | ... |
| servico_pedidos | 5004 | pedidos.db | ... |

## Integrações
| # | Tipo | Quem chama | Quem responde | Rota usada | O que faz |
|---|---|---|---|---|---|
| 1 | Busca | ... | ... | GET ... | ... |
| 2 | Busca | ... | ... | GET ... | ... |
| 3 | Alteração | ... | ... | POST/PUT ... | ... |

## Como executar
1. `py -m venv .venv` e `.venv\Scripts\Activate.ps1`
2. `pip install -r requirements.txt`
3. No VS Code: Executar e Depurar > **Iniciar os 4 serviços**
4. Importar `thunder-client-colecao.json` no Thunder Client

## Publicação (Render)
> Links dos serviços publicados.
