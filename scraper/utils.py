import json
import unicodedata
from collections.abc import Callable
from dataclasses import dataclass
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from constantes import URL_PESSOA_BUSCAR
from entidades.pessoa import Pessoa


# Para conversão da lista_pessoa em pessoa
@dataclass(slots=True)
class PessoaSite:
    nome: str | None
    id_site: str | None


# Acessa um link e extrai o conteúdo HTML da página
def extrair_pagina(link: str) -> BeautifulSoup:
    req = requests.get(link)
    return BeautifulSoup(req.text, "html.parser")


# Unifica todas as strings que estão no elemento (direta ou indiretamente) com "\n"
def inserir_enter(elemento: Tag | str) -> str:
    if not isinstance(elemento, Tag):
        return elemento
    if elemento.name == "br":
        return "\n"
    return "".join(inserir_enter(el) for el in elemento.children)


# Retorna um lambda que verifica se um elemento contém exatamente a string buscada
def contem_str(palavra: str) -> Callable[[Tag], bool]:
    return lambda el: el.string == el.parent.string and el.string.strip() == palavra


# Normaliza uma string para caracteres unicode
# Útil para inserir strings com caracteres especiais como busca em links
def normalizar(texto: str) -> str:
    normalizado = unicodedata.normalize("NFD", texto)
    return "".join(c for c in normalizado if unicodedata.category(c) != "Mn")


# Busca uma pessoa pelo nome no sistema MUNDUS
def buscar_pessoas_por_nome_mundus(pessoa: str) -> list[Pessoa]:
    # Formata a string
    txt_busca = "+".join(quote(p, encoding="latin-1") for p in pessoa.split(" "))
    # Extração
    soup = extrair_pagina(URL_PESSOA_BUSCAR(txt_busca))
    resultados = soup.select("table.table_list tr:not(:first-child)")
    # Parsa os resultados
    lista = []
    for r in resultados:
        celulas = r.find_all("td")
        lista.append(Pessoa(celulas[1].a.text, celulas[0].text))
    return lista


# Obtém o NUSP de uma pessoa pelo nome no sistema MUNDUS
def obter_nusp_por_nome_mundus(nome: str) -> str | None:
    nome_formatado = "".join([c for c in nome if c.isalpha() or c in " -"])
    for r in buscar_pessoas_por_nome_mundus(nome_formatado):
        if normalizar(r.nome) == normalizar(nome):
            return r.nusp
    return None


# Escreve conteúdo em um arquivo JSON
def escrever_JSON(caminho: str, conteudo: list[dict]) -> None:
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(conteudo, f, ensure_ascii=False, indent=4)
