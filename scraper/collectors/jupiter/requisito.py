import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from bs4 import Tag

from constantes import Caminhos, URLJupiter
from entidades.requisito import Requisito, RequisitosDisciplina
from scraper.utils import escrever_JSON, extrair_pagina, inserir_enter


def ler_requisitos(pagina: Tag) -> list[dict[str, Any]]:

    requisitos = []
    # Para cada curso
    for curso in pagina.select('tr[bgcolor="#658CCF"] font'):
        # Informações sobre o curso
        txt = " ".join([s.strip() for s in inserir_enter(curso).split("\n")])
        codigo_curso = txt.split(" ")[1].strip()
        nome_curso = " - ".join(txt.split("  ", 1)[1].split(" - ")[:-1]).strip()
        periodo_ideal = int(txt.split(" ")[-1])

        # Leitura dos requisitos
        id_grupo = 0  # Identificar disciplinas que têm conjuntos de requisitos 'OU'
        tr = curso.parent.parent.next_sibling
        while True:
            tr = tr.next_sibling
            if tr.name != "tr":  # Se for uma linha em branco
                continue
            if not tr.get("valign"):  # Se for o fim da lista
                break
            if tr.b and tr.b.text == "ou":  # Se for um novo conjunto de requisitos
                id_grupo += 1
                continue

            # Então é uma tag válida para um requisito
            nome_completo_disc = tr.find("td").text.split(" - ", 1)
            requisito = Requisito(
                codigo_curso=codigo_curso,
                nome_curso=nome_curso,
                periodo_ideal=periodo_ideal,
                id_grupo=id_grupo,
                codigo_requisito=nome_completo_disc[0].strip(),
                nome_requisito=nome_completo_disc[1].strip(),
                tipo=tr.find("font").text.strip(),
            )
            requisitos.append(requisito)

    return requisitos


def main() -> None:
    print("LENDO requisitos de disciplinas do Jupiter")

    # Itera sobre todos os .json na pasta
    for arquivo in Path(Caminhos.PASTA_DISCS).glob("*.json"):
        codigo_uni = arquivo.stem

        # Se o arquivo já existe, pula
        if Path(Caminhos.REQ(codigo_uni)).exists():
            print(f"PULADO {codigo_uni}: arquivo já existe!")
            continue

        # Abre o arquivo .json correspondente às disciplinas da unidade
        with open(arquivo, encoding="utf-8") as file:
            discs = json.load(file)

            lista = []
            # Para cada uma das discipinas
            for disc in discs:
                codigo_disc = disc.get("codigo")  # Obtém o código
                # Extração
                soup = extrair_pagina(URLJupiter.REQUISITOS(codigo_disc))
                paginas = soup.select('form[name="form1"] table[bgcolor="#FFFFFF"]')
                requisitos = [] if not paginas else ler_requisitos(paginas[0])
                lista.append(asdict(RequisitosDisciplina(codigo_disc, requisitos)))

                print(f"LIDO {codigo_disc}")

        # Escreve no JSON
        escrever_JSON(Caminhos.REQ(codigo_uni), lista)
        print(f"ESCRITO no arquivo JSON da unidade {codigo_uni}")


if __name__ == "__main__":
    main()
