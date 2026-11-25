import json
from dataclasses import asdict
from typing import Any

import requests

from constantes import URL_PROXY_PORTAL_SERVICOS, URLICMC, Caminhos
from entidades.comissao import Comissao, MembroComissao
from scraper.utils import escrever_JSON, extrair_pagina


# Converte os dados brutos do request
def converter_dados_do_request(dados: dict[str, Any]) -> MembroComissao:
    return MembroComissao(
        nome=dados["nompes"],
        nusp=dados["codpes"],
        categ_colegiado=dados["grupo1"].split(":", 1)[1],
        func_colegiado=dados["tipfncclg"],
        func_membro=dados["grupo2"],
        inicio_mandato=dados["dtainimdtfmt"],
        fim_mandato=dados["dtafimmdtfmt"],
    )


def main() -> None:
    print("LENDO comissões do ICMC")

    # Coleta todas as comissões
    soup = extrair_pagina(URLICMC.COMISSOES)
    elementos = soup.select("#cck70_value_art_introtext > h4:nth-child(8) ~ ul li a")

    comissoes = []
    # Para cada uma das comissões
    for el in elementos:
        link = el.get("href")
        if "mandato" not in link:  # Se o link não é uma página de mandatos
            continue

        nome = el.text
        # Realiza um request para obter os dados
        cod = link.split("/")[-2]
        sigla = link.split("/")[-1]
        req = requests.post(
            URL_PROXY_PORTAL_SERVICOS, json={"codclg": cod, "sglclg": sigla, "difref": "0"}
        )

        if req.status_code != 200:  # Se o request não funcionou
            continue
        if not (dados_brutos_comissao := json.loads(req.text)):  # Se não deu resultados
            continue

        # Adiciona os resultados formatados à lista
        membros = [converter_dados_do_request(d) for d in dados_brutos_comissao]
        comissoes.append(asdict(Comissao(nome, link, cod, sigla, membros)))

        print(f"LIDO comissão {nome}")

    # Escreve no JSON
    escrever_JSON(Caminhos.COMISSOES, comissoes)
    print("ESCRITO no arquivo JSON")


if __name__ == "__main__":
    main()
