import json

from db.conexao import conectar
from db.read.prox import buscar_por_proximidade
from entidades.disciplina import Disciplina
from entidades.oferecimento import HorarioOfcProfessor, Oferecimento
from entidades.requisito import Requisito


# Retorna no máximo uma disciplina de acordo com um código fornecido
def buscar_disc_por_codigo(codigo: str) -> Disciplina | None:
    with conectar() as conn:
        sql = "SELECT dados FROM disciplina WHERE codigo = ?"
        res = conn.execute(sql, (codigo,)).fetchone()

        return {} if not res else Disciplina.from_dict(json.loads(res[0]))


def buscar_discs_por_nome(nome: str) -> tuple[bool, list[Disciplina]]:
    # Realiza a busca e retorna
    auto_sugerir, res = buscar_por_proximidade(nome, "disciplina", "nome", ["dados"])
    res_formatado = [Disciplina.from_dict(json.loads(r["dados"])) for r in res]

    return auto_sugerir, res_formatado


# Busca todos os oferecimentos de um professor pelo seu nome
def buscar_horarios_por_nome_prof(nome: str) -> list[HorarioOfcProfessor]:
    with conectar() as conn:
        sql = """
            SELECT disciplina.nome, disc_ofc.codigo_disciplina, disc_ofc.codigo_turma, disc_ofc.obs, disc_ofc_horario.dados
            FROM disc_ofc_horario
            JOIN disc_ofc_horario_prof ON disc_ofc_horario.id = disc_ofc_horario_prof.id_horario
            JOIN disc_ofc ON disc_ofc.codigo_disciplina = disc_ofc_horario.codigo_disciplina AND disc_ofc.codigo_turma = disc_ofc_horario.codigo_turma
            JOIN disciplina ON disciplina.codigo = disc_ofc_horario_prof.codigo_disciplina
            WHERE disc_ofc_horario_prof.nome = ?
        """
        res = conn.execute(sql, (nome,)).fetchall()
        return [HorarioOfcProfessor.from_tupla(tupla) for tupla in res]


# Retorna uma lista dos requisitos de uma disciplina
def buscar_requisitos_por_codigo_disc(cod: str) -> list[Requisito]:
    with conectar() as conn:
        sql = "SELECT dados FROM disciplina_requisito WHERE codigo_disciplina = ?"
        res = conn.execute(sql, (cod,)).fetchall()
        return [] if not res else [Requisito(**json.loads(r[0])) for r in res]


# Retorna uma lista dos oferecimentos de uma disciplina
def buscar_oferecimentos_por_codigo_disc(cod: str) -> list[Oferecimento]:
    with conectar() as conn:
        sql = "SELECT dados FROM disc_ofc WHERE codigo_disciplina = ?"
        res = conn.execute(sql, (cod,)).fetchall()
        return [] if not res else [Oferecimento.from_dict(json.loads(r[0])) for r in res]
