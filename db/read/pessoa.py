import json

from db.conexao import conectar
from db.read.prox import buscar_por_proximidade
from entidades.pessoa import PessoaICMC


# Retorna o email de uma pessoa com o nusp fornecido
def obter_email_da_pessoa_por_nusp(nusp: str) -> str | None:
    with conectar() as conn:
        sql = "SELECT email FROM pessoa WHERE nusp = ?"
        res = conn.execute(sql, (nusp,)).fetchone()

        return None if not res else res[0]


# Retorna no máximo uma pessoa com o nusp fornecido
def buscar_pessoa_por_nusp(nusp: str) -> PessoaICMC:
    with conectar() as conn:
        sql = "SELECT dados FROM pessoa WHERE nusp = ?"
        res = conn.execute(sql, (nusp,)).fetchall()

        return None if not res else PessoaICMC.from_dict(json.loads(res[0]))


# Retorna no máximo uma pessoa com o id fornecido
def buscar_pessoa_por_id(id: str) -> PessoaICMC:
    with conectar() as conn:
        sql = "SELECT dados FROM pessoa WHERE id = ?"
        res = conn.execute(sql, (id,)).fetchone()

        return None if not res else PessoaICMC.from_dict(json.loads(res[0]))


def buscar_pessoas_por_nome(nome: str) -> tuple[bool, list[PessoaICMC]]:
    # Realiza a busca e retorna
    auto_sugerir, res = buscar_por_proximidade(nome, "pessoa", "nome", ["dados"])
    pessoas = [PessoaICMC.from_dict(json.loads(r["dados"])) for r in res]

    return auto_sugerir, pessoas
