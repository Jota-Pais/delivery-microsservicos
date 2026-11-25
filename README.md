# Delivery em Microsserviços

**Equipe:** Arthur Santin, Gabriel Ugione e João Carlos Pais

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
10. O sistema deve permitir listar e consultar pedidos e cancelar um pedido, liberando o entregador.

## Descritivo técnico

| Microsserviço | Porta | Banco | Função | Campos principais | Quem programa |
|---|---|---|---|---|---|
| servico_clientes | 5001 | clientes.db | Cadastro de clientes e consulta "está ativo?" | nome, telefone, endereco, ativo, criado_em | Arthur Santin |
| servico_cardapio | 5002 | cardapio.db | Cadastro de pratos e fornecimento de preço e disponibilidade | nome, preco, ativo, criado_em | Gabriel Ugione |
| servico_entregadores | 5003 | entregadores.db | Cadastro de entregadores e controle ocupado/livre | nome, veiculo, disponivel, ativo, criado_em | Arthur Santin |
| servico_pedidos | 5004 | pedidos.db | Registro dos pedidos, orquestrando os outros três serviços | cliente_id, prato_id, entregador_id, valor, status, criado_em | Gabriel Ugione |

Cada serviço tem seu banco SQLite, seu `requirements.txt` e uma rota `/api/health`. Um serviço nunca abre o banco de outro: o pedidos guarda apenas os ids (`cliente_id`, `prato_id`, `entregador_id`), sem chave estrangeira, e consulta os outros serviços por HTTP.

Clientes, cardápio e entregadores recriam dados iniciais ao ligar se o banco estiver vazio (no Render o banco é apagado quando o serviço hiberna): cliente 1 ativo e cliente 2 inativo; prato 1 ativo e prato 2 inativo; entregadores 1 e 2 ativos e livres. O pedidos não cria dados iniciais, porque um pedido só existe depois de conversar com os outros três serviços.

## Integrações
| # | Tipo | Quem chama | Quem responde | Rota usada | O que faz | E se o outro estiver fora do ar? |
|---|---|---|---|---|---|---|
| 1 | Busca | pedidos | clientes | GET /api/clientes/<id>/ativo | Confere se o cliente existe e está ativo | O pedido é recusado (400) com "O serviço CLIENTES está indisponível"; nada é gravado |
| 2 | Busca | pedidos | cardapio | GET /api/pratos/<id> | Obtém o preço e se o prato está disponível | O pedido é recusado (400) com "O serviço CARDAPIO está indisponível"; nada é gravado |
| 3 | Alteração | pedidos | entregadores | PATCH /api/entregadores/<id>/ocupar | Marca o entregador como ocupado | O pedido já gravado é apagado (compensação) e o erro é devolvido (400). O mesmo acontece se o entregador estiver ocupado ou inativo |

Todas as chamadas usam timeout de 5 segundos (`integracao.py`), para não esperar para sempre por um serviço lento.

### Fluxo de um pedido (POST /api/pedidos)
1. Pergunta ao **clientes** se o cliente está ativo.
2. Pergunta ao **cardápio** o preço do prato e se ele está disponível.
3. Grava o pedido no próprio banco (`pedidos.db`) com o valor e o status "confirmado".
4. Pede ao **entregadores** para ocupar o entregador. Se ele recusar ou estiver fora do ar, o pedido é apagado (compensação), porque cada serviço tem o seu banco e não existe "desfazer tudo" automático.

Cancelar um pedido (`PATCH /api/pedidos/<id>/cancelar`) libera o entregador.

## Como executar
1. `py -m venv .venv`
2. Ativar o ambiente: `.venv\Scripts\Activate.ps1` (PowerShell) ou `.venv\Scripts\activate.bat` (Prompt de Comando)
3. `pip install -r requirements.txt`
4. No VS Code: Executar e Depurar > **Iniciar os 4 serviços** (ou dois cliques em `iniciar_servicos.bat`)
5. Testar:
   - **Thunder Client:** importar `thunder-client-colecao.json` e os ambientes de `thunder-ambientes/` (Local e Render) e selecionar o ambiente ativo. A pasta "Integrações" tem os casos do pedido.
   - **REST Client:** abrir `testes-integracoes.http` (integrações) ou `testes-cardapio.http` e clicar em **Send Request**.

### Casos de teste das integrações
| Caso | Pedido | Resultado esperado |
|---|---|---|
| 1. Pedido válido | cliente 1, prato 1, entregador 2 | 201, entregador 2 fica ocupado |
| 2. Cliente inativo | cliente 2 | 400 "Cliente inativo." |
| 3. Prato inativo | prato 2 | 400 "Prato indisponível." |
| 4. Entregador ocupado | entregador 2 de novo | 400 e o pedido é desfeito (compensação) |
| 5. Serviço fora do ar | parar o cardápio | 400 "O serviço CARDAPIO está indisponível" |

No Render, as variáveis `CLIENTES_URL`, `CARDAPIO_URL` e `ENTREGADORES_URL` do serviço de pedidos apontam para os endereços públicos dos outros serviços.

## Divisão do trabalho
| Integrante | Responsabilidades |
|---|---|
| Arthur Santin | servico_clientes e servico_entregadores (incluindo ocupar e liberar) |
| Gabriel Ugione | servico_cardapio, servico_pedidos (as 3 integrações e a compensação), coleção de testes e publicação no Render |
| João Carlos Pais | Planejamento da arquitetura, contrato entre os serviços (rotas e campos), repositório no GitHub e coordenação da equipe |

## Publicação (Render)
| Serviço | Link |
|---|---|
| servico_clientes | https://delivery-clientes.onrender.com/api/clientes |
| servico_cardapio | https://delivery-cardapio.onrender.com/api/pratos |
| servico_entregadores | https://delivery-entregadores.onrender.com/api/entregadores |
| servico_pedidos | https://delivery-pedidos.onrender.com/api/pedidos |

> Plano gratuito: os serviços hibernam após 15 minutos sem uso e a primeira chamada pode levar cerca de 50 segundos. Antes de testar, abra o `/api/health` de cada serviço.
