import json

from db.conexao import conectar
from db.read.pessoa import obter_email_da_pessoa_por_nusp
from db.read.prox import buscar_por_proximidade
from entidades.comissao import Chapa, Comissao, MembroComissao


# Retorna no máximo uma comissão de acordo com o código e sigla fornecidos
def buscar_comissao_por_cod_e_sigla(codigo: str, sigla: str) -> Comissao | None:
    with conectar() as conn:
        sql = "SELECT dados FROM comissao WHERE codigo = ? AND sigla = ?"
        res = conn.execute(sql, (codigo, sigla)).fetchone()

        return None if not res else Comissao.from_dict(json.loads(res[0]))


def buscar_comissoes_por_nome(nome: str) -> tuple[bool, list[Comissao]]:
    # Realiza a busca e retorna
    auto_sugerir, res = buscar_por_proximidade(nome, "comissao", "nome", ["dados"])
    comissoes = [Comissao.from_dict(json.loads(r["dados"])) for r in res]

    return auto_sugerir, comissoes


# Obtém a presidência de uma comissão de acordo com o código e sigla fornecidos
# Também retorna o email do presidente e vice
def obter_presidencia_por_cod_e_sigla(codigo: str, sigla: str) -> Chapa:
    with conectar() as conn:
        sql = "SELECT dados FROM comissao WHERE codigo = ? AND sigla = ?"
        res = conn.execute(sql, (codigo, sigla)).fetchone()
        comissao = Comissao.from_dict(json.loads(res[0]))

        # Obtém a presidência
        chapa = comissao.obter_presidencia()
        if chapa.pres is not None:
            chapa.pres.email = obter_email_da_pessoa_por_nusp(chapa.pres.nusp)
        if chapa.vice is not None:
            chapa.vice.email = obter_email_da_pessoa_por_nusp(chapa.vice.nusp)

        return chapa


# Retorna os representantes discentes de uma comissão, se houver
def obter_representantes_discentes(codigo: str, sigla: str) -> list[MembroComissao] | None:
    with conectar() as conn:
        sql = "SELECT dados FROM comissao_membro WHERE codigo_comissao = ? AND sigla_comissao = ? AND categoria_coleg = 'Representante Discente de Graduação'"
        res = conn.execute(sql, (codigo, sigla)).fetchall()

        return [MembroComissao(**json.loads(r[0])) for r in res]
