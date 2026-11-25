import json

from db.conexao import conectar
from db.read.prox import buscar_por_proximidade
from entidades.pesquisa import Pesquisa


# Busca uma pesquisa por um ID
def buscar_pesquisa_por_id(id: str) -> Pesquisa:
    with conectar() as conn:
        sql = "SELECT dados FROM pesquisa WHERE id = ?"
        res = conn.execute(sql, (id,)).fetchone()

        return None if not res else Pesquisa.from_dict(json.loads(res[0]))


# Retorna uma lista de nomes de pesquisas de que uma pessoa faz parte
def buscar_pesquisas_por_id_pessoa(id: str) -> list[str]:
    with conectar() as conn:
        sql = """
            SELECT pesquisa.nome
            FROM pesquisa
            JOIN pesquisa_pessoa ON pesquisa_pessoa.id_pesquisa = pesquisa.id
            JOIN pessoa ON pessoa.id = pesquisa_pessoa.id_pessoa
            WHERE pessoa.id = ?
        """
        res = conn.execute(sql, (id,)).fetchall()
        return [r[0] for r in res]


# Realiza uma busca de pesquisa por seu nome
def buscar_pesquisas_por_nome(nome: str) -> tuple[bool, list[Pesquisa]]:
    auto_sugerir, res = buscar_por_proximidade(nome, "pesquisa", "nome", ["dados"])
    pesquisas = [Pesquisa.from_dict(json.loads(r["dados"])) for r in res]

    return auto_sugerir, pesquisas
