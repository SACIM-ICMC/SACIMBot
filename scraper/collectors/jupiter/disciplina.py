from dataclasses import asdict
from pathlib import Path

from bs4 import Tag

from constantes import Caminhos, URLJupiter
from entidades.disciplina import Disciplina
from entidades.pessoa import Pessoa
from scraper.utils import contem_str, escrever_JSON, extrair_pagina, inserir_enter


# Leitura de elementos da página
def obter_infos_unidade(pagina: Tag) -> tuple[str | None]:
    tag = pagina.table.td.find_all("table", recursive=False)[2]
    lista_strings = [inserir_enter(s) for s in tag.find_all("span")]

    return (
        lista_strings[0].strip(),  # unidade
        lista_strings[1].strip(),  # departamento
        lista_strings[2].split(" ")[1].strip(),  # codigo
        lista_strings[2].split(" - ", 1)[1].strip(),  # nome
        None if len(lista_strings) < 4 else lista_strings[3].strip(),  # nome_ingles
    )


def obter_valor_str_do_campo(pagina: Tag, campo: str) -> str:
    if (tag := pagina.find(string=contem_str(campo + ":"))) is None:
        raise ValueError(f"Campo obrigatório não encontrado: {campo}")
    return tag.find_parent("td").next_sibling.next_sibling.get_text().strip()


def obter_valor_int_do_campo(pagina: Tag, campo: str) -> int:
    # Transforma "60 h" em 60 se necessário
    return int(obter_valor_str_do_campo(pagina, campo).split()[0])


def obter_valor_str_opc_do_campo(pagina: Tag, campo: str) -> str | None:
    if (tag := pagina.find(string=contem_str(campo + ":"))) is None:
        return None
    return tag.find_parent("td").next_sibling.next_sibling.get_text().strip()


def obter_valor_int_opc_do_campo(pagina: Tag, campo: str) -> int | None:
    val = obter_valor_str_opc_do_campo(pagina, campo)
    return int(val.split()[0]) if val else None  # Transforma "60 h" em 60 se necessário


def obter_conteudo_da_secao(pagina: Tag, secao: str) -> str | None:
    if (tag := pagina.find(string=contem_str(secao))) is None:
        return None
    return inserir_enter(tag.find_parent("tr").next_sibling.next_sibling.pre).strip()


def obter_conteudo_da_subsecao(pagina: Tag, subsecao: str) -> str | None:
    if (tag := pagina.find(string=contem_str(subsecao))) is None:
        return None
    return inserir_enter(tag.find_parent("tr").next_sibling.next_sibling.span).strip()


def obter_bibliografia(pagina: Tag) -> str | None:
    secoes = (
        ("Bibliografia", ""),
        ("Bibliografia Básica", "BIBLIOGRAFIA BÁSICA\n"),
        ("Bibliografia Complementar", "BIBLIOGRAFIA COMPLEMENTAR\n"),
    )

    textos = []
    for secao, prefixo in secoes:
        if (tag := pagina.find(string=contem_str(secao))) is None:
            continue
        textos.append(prefixo + inserir_enter(tag.find_parent("table").pre).strip())
    return "\n".join(textos) or None


def obter_docentes_responsaveis(pagina: Tag) -> list[Pessoa]:
    if (tag := pagina.find(string=contem_str("Docente(s) Responsável(eis)"))) is None:
        return []

    elementos = tag.find_parent("table").select("table tr td:nth-child(2) span")
    pessoas = []
    for elemento in elementos:
        nome, nusp = elemento.string.split(" - ", 1)
        pessoas.append(Pessoa(nome.strip(), nusp.strip()))
    return pessoas


def ler_disciplina(pagina: Tag) -> Disciplina:

    return Disciplina(
        *obter_infos_unidade(pagina),
        # Campos
        tipo=obter_valor_str_do_campo(pagina, "Tipo"),
        data_ativacao=obter_valor_str_do_campo(pagina, "Ativação"),
        data_desativacao=obter_valor_str_opc_do_campo(pagina, "Desativação"),
        creditos_aula=obter_valor_int_do_campo(pagina, "Créditos Aula"),
        creditos_trab=obter_valor_int_do_campo(pagina, "Créditos Trabalho"),
        carga_horaria=obter_valor_int_do_campo(pagina, "Carga Horária Total"),
        carga_horaria_extensao=obter_valor_int_opc_do_campo(pagina, "Carga Horária de Extensão"),
        # Seção de atividades de extensão
        grupos_ext=obter_conteudo_da_subsecao(pagina, "Grupo social alvo da atividade"),
        objetivos_ext=obter_conteudo_da_subsecao(pagina, "Objetivos da atividade"),
        descricao_ext=obter_conteudo_da_subsecao(pagina, "Descrição da atividade"),
        indicadores_ext=obter_conteudo_da_subsecao(pagina, "Indicadores de avaliação da atividade"),
        # Seção de conteúdo da disciplina
        ementa=obter_conteudo_da_secao(pagina, "Ementa"),
        objetivos=obter_conteudo_da_secao(pagina, "Objetivos"),
        conteudo=obter_conteudo_da_secao(pagina, "Conteúdo Programático"),
        # Seção de métodos e critérios de avaliação
        metodo_avaliacao=obter_conteudo_da_subsecao(pagina, "Método de Avaliação"),
        criterios_avaliacao=obter_conteudo_da_subsecao(pagina, "Critério de Avaliação"),
        recuperacao=obter_conteudo_da_subsecao(pagina, "Norma de Recuperação"),
        bibliografia=obter_bibliografia(pagina),
        docentes_responsaveis=obter_docentes_responsaveis(pagina),
    )


def main() -> None:
    print("LENDO lista de disciplinas da USP")

    # Coleta todos os códigos das unidades
    soup = extrair_pagina(URLJupiter.UNIDADES)
    res = soup.select('#layout_conteudo tr[bgcolor="#658CCF"] ~ tr td:first-child span')

    codigos_unidades = [r.string.strip() for r in res]

    # Para cada um dos códigos de unidades coletados
    for codigo_unidade in codigos_unidades:
        # Se o arquivo existe, pula
        if Path(Caminhos.DISC(codigo_unidade)).exists():
            print(f"PULADO {codigo_unidade}: arquivo já existe!")
            continue

        # Acessa o link para obter os códigos das disciplinas
        soup = extrair_pagina(URLJupiter.DISCIPLINAS_DA_UNIDADE(codigo_unidade))
        res = soup.select('#layout_conteudo tr[bgcolor="#658CCF"] ~ tr td:first-child span')

        codigos_disciplinas = [r.string.strip() for r in res]

        disciplinas = []
        # Para cada um dos códigos de disciplinas coletados,
        for codigo_disciplina in codigos_disciplinas:
            # Acessa o link para obter os dados da disciplina
            soup = extrair_pagina(URLJupiter.DISCIPLINA(codigo_disciplina))

            # Obtém o conteúdo da página
            pagina = soup.select('form[name="form1"]')
            if not pagina:
                print(f"PULADO {codigo_disciplina}: não existe no Jupiter")
                continue

            disciplinas.append(asdict(ler_disciplina(pagina[0])))

            print(f"LIDO {codigo_disciplina}")

        # Escreve no JSON
        escrever_JSON(Caminhos.DISC(codigo_unidade), disciplinas)
        print(f"ESCRITO no arquivo JSON da unidade {codigo_unidade}")


if __name__ == "__main__":
    main()
