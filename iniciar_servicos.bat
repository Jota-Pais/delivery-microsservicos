
@echo off
REM Abre 4 janelas, uma para cada servico (alternativa ao VS Code).
for %%P in (servico_clientes servico_cardapio servico_entregadores servico_pedidos) do (
  start "%%P" cmd /k "cd /d %~dp0%%P && py app.py"
)
