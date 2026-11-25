import json
from dataclasses import asdict
from pathlib import Path

from bs4 import Tag

from constantes import Caminhos, URLJupiter
from entidades.oferecimento import (
    DocenteTabelaAtiv,
    DocenteTabelaHorario,
    Horario,
    Oferecimento,
    OferecimentosDisciplina,
)
from scraper.utils import escrever_JSON, extrair_pagina


def celula_linha(tr: Tag, coluna: int) -> str | None:
    # Verificações
    if coluna < 0 or len(tds := tr.find_all("td")) <= coluna:
        return None

    el = tds[coluna].span
    return None if not el else (el.text.strip() or None)


def celula_tabela(tabela: Tag, linha: int, coluna: int) -> str | None:
    # Verificações
    if linha < 0 or len(trs := tabela.find_all("tr")) <= linha:
        return None
    return celula_linha(trs[linha], coluna)


# Extrai o tipo que está ou no começo ou no final da string
def extrair_nome_e_tipo(txt: str) -> tuple[str | None, str | None]:
    if not txt:
        return None, None
    if txt.startswith("("):
        return txt[4:], txt[1]
    if txt.endswith(")"):
        return txt[:-4], txt[-2]
    return txt, None


def ler_tabela(tabela: Tag, oferecimento: Oferecimento) -> None:
    titulo = tabela.find("tr").span.text
    trs = tabela.find_all("tr")

    # Tabela de atividades
    if "Atividades" in titulo:
        for tr in trs[2:]:  # Pula os cabeçalhos
            # Obtém o professor
            prof = DocenteTabelaAtiv(
                *extrair_nome_e_tipo(celula_linha(tr, 3)),
                tipo_atividade=celula_linha(tr, 1),
                carga_horaria=int(ch) if (ch := celula_linha(tr, 2)) else None,
            )
            oferecimento.atividades.append(prof)
        return

    # Tabela de horários
    if "Horário" in titulo:
        for tr in trs[1:]:  # Pula o cabeçalho
            # Obtém o professor
            prof = DocenteTabelaHorario(*extrair_nome_e_tipo(celula_linha(tr, 3)))
            # Se o tr for uma linha de um único professor
            if not celula_linha(tr, 0):
                # Adiciona no último horário lido
                oferecimento.horarios[-1].professores.append(prof)
                return

            horario = Horario(celula_linha(tr, 0), celula_linha(tr, 1), celula_linha(tr, 2), [prof])
            oferecimento.horarios.append(horario)
        return

    # Não tem mais tabela (é a última)
    if tabela.select('tr[bgcolor="#658CCF"]'):
        return

    raise Exception("Existência de tabela não identificada!")


def ler_oferecimento(of: Tag) -> Oferecimento:
    tabelas = of.select("table")  # Obtém a lista de tabelas

    # Dados da primeira tabela
    tabela = tabelas[0]
    txt_cod = celula_tabela(tabela, 0, 1).split(" ", 1)
    oferecimento = Oferecimento(
        codigo_turma=txt_cod[0] or None,
        obs_turma=None if len(txt_cod) == 1 else " ".join(txt_cod[1:]),
        inicio=celula_tabela(tabela, 1, 1),
        fim=celula_tabela(tabela, 2, 1),
        tipo=celula_tabela(tabela, 3, 1),
        obs=celula_tabela(tabela, 4, 1),
        horarios=[],
        atividades=[],
    )
    # Restante das tabelas
    for tabela in tabelas[1:]:
        ler_tabela(tabela, oferecimento)

    return oferecimento


def ler_oferecimentos(pg: Tag) -> list[Oferecimento]:
    return [ler_oferecimento(of) for of in pg.findChildren("div", recursive=False)]


def main() -> None:
    print("LENDO oferecimentos de disciplinas do Jupiter")

    # Itera sobre todos os .json na pasta
    pasta = Path(Caminhos.PASTA_DISCS)
    for arquivo in pasta.glob("*.json"):
        codigo_uni = arquivo.stem

        # Se o arquivo já existe na pasta /oferecs, pula
        if Path(Caminhos.OFC(codigo_uni)).exists():
            print(f"PULADO {codigo_uni}: arquivo já existe!")
            continue

        # Abre o arquivo .json correspondente às disciplinas da unidade
        with open(arquivo, encoding="utf-8") as f:
            discs = json.load(f)
            lista = []
            # Para cada uma das discipinas
            for d in discs:
                codigo_disc = d.get("codigo")  # Obtém o código
                # Extração
                soup = extrair_pagina(URLJupiter.OFERECIMENTOS(codigo_disc))  # Conecta
                paginas = soup.select('td[width="568"]')
                oferecimentos = [] if not paginas else ler_oferecimentos(paginas[0])
                lista.append(asdict(OferecimentosDisciplina(codigo_disc, oferecimentos)))

                print(f"LIDO {codigo_disc}")

        # Escreve no JSON
        escrever_JSON(Caminhos.OFC(codigo_uni), lista)
        print(f"ESCRITO no arquivo JSON da unidade {codigo_uni}")


if __name__ == "__main__":
    main()
