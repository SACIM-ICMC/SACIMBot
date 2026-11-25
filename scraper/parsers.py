import json
import sys
from pathlib import Path

import db.write as w
from constantes import Caminhos
from entidades.comissao import Comissao
from entidades.curso import Curso
from entidades.disciplina import Disciplina
from entidades.oferecimento import OferecimentosDisciplina
from entidades.pesquisa import Pesquisa
from entidades.pessoa import PessoaICMC
from entidades.requisito import RequisitosDisciplina


def parse_comissoes() -> None:
    with open(Caminhos.COMISSOES) as file:
        # Insere as comissões
        w.inserir_comissoes([Comissao.from_dict(c) for c in json.load(file)])


def parse_cursos() -> None:
    with open(Caminhos.CURSOS) as file:
        # Insere os cursos
        w.inserir_cursos([Curso(**c) for c in json.load(file)])


def parse_disciplinas() -> None:
    # Itera sobre todos os .json na pasta
    for arquivo in Path(Caminhos.PASTA_DISCS).glob("*.json"):
        # Abre o arquivo .json correspondente às disciplinas da unidade
        with open(arquivo, encoding="utf-8") as file:
            # Insere as disciplinas
            w.inserir_disciplinas(arquivo.stem, [Disciplina.from_dict(d) for d in json.load(file)])


def parse_oferecimentos() -> None:
    # Itera sobre todos os .json na pasta
    for arquivo in Path(Caminhos.PASTA_OFCS).glob("*.json"):
        # Abre o arquivo .json correspondente às disciplinas da unidade
        with open(arquivo, encoding="utf-8") as file:
            # Insere os oferecimentos
            w.inserir_oferecimentos(
                [OferecimentosDisciplina.from_dict(ofc) for ofc in json.load(file)]
            )


def parse_pesquisa() -> None:
    with open(Caminhos.PESQUISAS) as file:
        # Insere as pesquisas
        w.inserir_pesquisas([Pesquisa.from_dict(p) for p in json.load(file)])


def parse_pessoa() -> None:
    with open(Caminhos.PESSOAS) as file:
        # Insere as pessoas
        w.inserir_pessoas([PessoaICMC.from_dict(p) for p in json.load(file)])


def parse_requisitos() -> None:
    # Itera sobre todos os .json na pasta
    for arquivo in Path(Caminhos.PASTA_REQS).glob("*.json"):
        # Abre o arquivo .json correspondente às disciplinas da unidade
        with open(arquivo, encoding="utf-8") as file:
            # Insere os requisitos
            w.inserir_requisitos([RequisitosDisciplina.from_dict(r) for r in json.load(file)])


# Para definição dos parsers
match sys.argv[1]:
    case "comissao":
        parse_comissoes()
    case "cursos":
        parse_cursos()
    case "disciplina":
        parse_disciplinas()
    case "oferecimento":
        parse_oferecimentos()
    case "pesquisa":
        parse_pesquisa()
    case "pessoa":
        parse_pessoa()
    case "requisito":
        parse_requisitos()
