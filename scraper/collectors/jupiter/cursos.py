import re
from dataclasses import asdict

from constantes import Caminhos, URLJupiter
from entidades.curso import Curso
from scraper.utils import escrever_JSON, extrair_pagina


def main() -> None:
    print("LENDO cursos da USP")

    # Coleta todos os códigos das unidades
    soup = extrair_pagina(URLJupiter.UNIDADES)
    res = soup.select('#layout_conteudo tr[bgcolor="#658CCF"] ~ tr')
    unidades = [(r.find_all("td")[0].string.strip(), r.a.text.strip()) for r in res]

    cursos = []
    # Para cada um dos códigos de unidades coletados,
    for codigo_unidade, nome_unidade in unidades:
        # acessa o link para obter a lista de cursos ativos
        soup = extrair_pagina(URLJupiter.CURSOS_DA_UNIDADE(codigo_unidade, "N"))
        res = soup.select('#layout_conteudo tr[bgcolor="#658CCF"] ~ tr')

        # Para cada curso
        for req in res:
            # Coleta os dados da página do curso
            cod_curso = re.search(r"codcur=(\d+)", req.a.get("href")).group(1).strip()
            cod_hab = re.search(r"codhab=(\d+)", req.a.get("href")).group(1).strip()
            # -2 porque a poli fez o favor de fazer a tabela diferente
            nome_curso = (req.find_all("td")[-2].span.text or req.find_all("td")[-2].a.text).strip()
            periodo = req.find_all("td")[-1].span.text.strip()

            curso = Curso(
                codigo_curso=cod_curso,
                codigo_habilitacao=cod_hab,
                codigo_unidade=codigo_unidade,
                nome=nome_curso,
                unidade=nome_unidade,
                periodo=periodo,
                ativado=1,
                link=URLJupiter.CURSO(codigo_unidade, cod_curso, cod_hab, "N"),
            )
            cursos.append(asdict(curso))
            print(f"LIDO {nome_curso}")

    # Escreve no JSON
    escrever_JSON(Caminhos.CURSOS, cursos)
    print("ESCRITO no arquivo JSON")


if __name__ == "__main__":
    main()
