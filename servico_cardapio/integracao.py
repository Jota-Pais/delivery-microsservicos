"""O "telefone" deste serviço para falar com os outros serviços.

Uso (dentro de regras.py):
    import integracao
    resposta = integracao.chamar("CLIENTES", "GET", "/api/clientes/1/ativo")

Os endereços podem ser trocados por variáveis de ambiente (útil no Render):
    CARDAPIO_URL=https://meu-servico2.onrender.com
"""
import os

import requests

from erros import RegraDeNegocioError

# Use 127.0.0.1 e não "localhost": no Windows, "localhost" pode tentar IPv6 antes
# e deixar a chamada lenta.
URLS = {
    "CLIENTES": os.environ.get("CLIENTES_URL", "http://127.0.0.1:5001"),
    "CARDAPIO": os.environ.get("CARDAPIO_URL", "http://127.0.0.1:5002"),
    "ENTREGADORES": os.environ.get("ENTREGADORES_URL", "http://127.0.0.1:5003"),
    "PEDIDOS": os.environ.get("PEDIDOS_URL", "http://127.0.0.1:5004"),
}
TIMEOUT = 5  # segundos: não esperar para sempre por um serviço lento
EU = "CARDAPIO"


def chamar(destino, metodo, caminho, **kwargs):
    """Faz a chamada HTTP e mostra no terminal. Se o destino falhar, vira erro 400 claro."""
    print(f"[{EU}]   >>> ligando para {destino}: {metodo} {caminho}", flush=True)
    try:
        resposta = requests.request(metodo, URLS[destino] + caminho, timeout=TIMEOUT, **kwargs)
    except requests.exceptions.ConnectionError:
        print(f"[{EU}]   <<< {destino} não atendeu (fora do ar?)", flush=True)
        raise RegraDeNegocioError(f"O serviço {destino} está indisponível. Tente mais tarde.")
    except requests.exceptions.Timeout:
        print(f"[{EU}]   <<< {destino} demorou demais (timeout)", flush=True)
        raise RegraDeNegocioError(f"O serviço {destino} demorou demais (timeout).")
    print(f"[{EU}]   <<< {destino} respondeu {resposta.status_code}", flush=True)
    return resposta
