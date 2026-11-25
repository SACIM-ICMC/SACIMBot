from sqlite3 import Cursor

from db.conexao import conectar
from entidades.comissao import Comissao
from entidades.curso import Curso
from entidades.disciplina import Disciplina
from entidades.oferecimento import Oferecimento, OferecimentosDisciplina
from entidades.pesquisa import Pesquisa
from entidades.pessoa import PessoaICMC
from entidades.requisito import RequisitosDisciplina

SQL_COM = "INSERT OR REPLACE INTO comissao VALUES (?, ?, ?, ?, ?)"
SQL_COM_MEMBRO = "INSERT OR REPLACE INTO comissao_membro VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
SQL_CURSO = "INSERT OR REPLACE INTO curso VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
SQL_DISC = """
    INSERT OR REPLACE INTO disciplina
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""
SQL_DISC_DOC_RESP = "INSERT OR REPLACE INTO disciplina_docente_responsavel VALUES (?, ?, ?)"
SQL_DISC_OFC = "INSERT OR REPLACE INTO disc_ofc VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
SQL_DISC_OFC_HORARIO = "INSERT OR REPLACE INTO disc_ofc_horario VALUES (NULL, ?, ?, ?, ?, ?, ?)"
SQL_DISC_OFC_HORARIO_PROF = "INSERT OR REPLACE INTO disc_ofc_horario_prof VALUES (?, ?, ?, ?, ?)"
SQL_DISC_OFC_ATIV = "INSERT OR REPLACE INTO disc_ofc_ativ VALUES (?, ?, ?, ?, ?, ?)"
SQL_DISC_REQ = "INSERT OR REPLACE INTO disciplina_requisito VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
SQL_PESQ = "INSERT OR REPLACE INTO pesquisa VALUES (?, ?, ?, ?)"
SQL_PESQ_PESSOA = "INSERT OR REPLACE INTO pesquisa_pessoa VALUES (?, ?)"
SQL_PESQ_LINHA = "INSERT OR REPLACE INTO pesquisa_linha VALUES (?, ?)"
SQL_PESQ_LAB = "INSERT OR REPLACE INTO pesquisa_lab VALUES (?, ?, ?)"
SQL_PESSOA = "INSERT OR REPLACE INTO pessoa VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"


def inserir_comissoes(comissoes: list[Comissao]) -> None:
    with conectar(False) as conn:
        cursor = conn.cursor()

        # Itera sobre as comissões
        for com in comissoes:
            cursor.execute(SQL_COM, com.gerar_linha_sql())
            # Para cada membro da comissão
            for m in com.membros:
                cursor.execute(SQL_COM_MEMBRO, (com.codigo, com.sigla, *m.gerar_linha_sql()))

        print(f"Escrito {len(comissoes)} comissão(ões).")
        conn.commit()


def inserir_cursos(cursos: list[Curso]) -> None:
    with conectar(False) as conn:
        cursor = conn.cursor()

        # Itera sobre os cursos e formata a lista
        for curso in cursos:
            cursor.execute(SQL_CURSO, curso.gerar_linha_sql())

        print(f"Escrito {len(cursos)} curso(s).")
        conn.commit()


def inserir_disciplinas(cod_uni: str, disciplinas: list[Disciplina]) -> None:
    with conectar(False) as conn:
        cursor = conn.cursor()

        # Itera sobre as disciplinas e formata a lista
        for d in disciplinas:
            # Tabela de disciplinas
            cursor.execute(SQL_DISC, (d.codigo, cod_uni, *d.gerar_linha_sql()))
            # Para cada docente responsavel
            for p in d.docentes_responsaveis:
                # Tabela de docentes responsáveis
                cursor.execute(SQL_DISC_DOC_RESP, (d.codigo, p.nome, p.nusp))

        print(f"Escrito {len(disciplinas)} disciplina(s).")
        conn.commit()


def inserir_oferecimento(ofc: Oferecimento, codigo_disc: str, cursor: Cursor) -> None:
    # Tabela principal
    cursor.execute(SQL_DISC_OFC, (codigo_disc, *ofc.gerar_linha_sql()))
    # Para cada horário oferecido
    for h in ofc.horarios:
        # Tabela com horários dos oferecimentos
        cursor.execute(SQL_DISC_OFC_HORARIO, (codigo_disc, ofc.codigo_turma, *h.gerar_linha_sql()))
        id_horario = cursor.lastrowid

        # Para cada professor do horário
        for p in h.professores:
            # Tabela dos professores de cada horário
            cursor.execute(
                SQL_DISC_OFC_HORARIO_PROF,
                (id_horario, codigo_disc, ofc.codigo_turma, p.nome, p.tipo),
            )
    # Para cada atividade oferecida
    for ativ in ofc.atividades:
        # Tabela das atividades de cada oferecimento
        cursor.execute(SQL_DISC_OFC_ATIV, (codigo_disc, ofc.codigo_turma, *ativ.gerar_linha_sql()))


def inserir_oferecimentos(disciplinas: list[OferecimentosDisciplina]) -> None:
    with conectar(False) as conn:
        cursor = conn.cursor()

        num_oferecimentos = 0
        # Para cada disciplina
        for disc in disciplinas:
            # Para cada oferecimento da disciplina
            for ofc in disc.oferecimentos:
                inserir_oferecimento(ofc, disc.codigo, cursor)
            num_oferecimentos += len(disc.oferecimentos)

        print(f"Escrito {num_oferecimentos} oferecimento(s).")
        conn.commit()


def inserir_requisitos(disciplinas: list[RequisitosDisciplina]) -> None:
    with conectar(False) as conn:
        cursor = conn.cursor()

        num_reqs = 0
        # Itera sobre os requisitos e formata a lista
        for req_disc in disciplinas:
            for req in req_disc.requisitos:
                cursor.execute(SQL_DISC_REQ, (req_disc.codigo, *req.gerar_linha_sql()))
            num_reqs += len(req_disc.requisitos)

        print(f"Escrito {num_reqs} requisito(s).")
        conn.commit()


def inserir_pesquisas(pesquisas: list[Pesquisa]) -> None:
    with conectar(False) as conn:
        cursor = conn.cursor()

        # Itera sobre as pesquisas e formata a lista
        for pesquisa in pesquisas:
            cursor.execute(SQL_PESQ, pesquisa.gerar_linha_sql())

            for linha in pesquisa.linhas:
                cursor.execute(SQL_PESQ_LINHA, (pesquisa.id_site, linha))
            for lab in pesquisa.labs:
                cursor.execute(SQL_PESQ_LAB, (pesquisa.id_site, lab.nome, lab.link))
            for pessoa in pesquisa.docentes:
                cursor.execute(SQL_PESQ_PESSOA, (pesquisa.id_site, pessoa.id_site))

        print(f"Escrito {len(pesquisas)} pesquisa(s).")
        conn.commit()


def inserir_pessoas(pessoas: list[PessoaICMC]) -> None:
    with conectar(False) as conn:
        cursor = conn.cursor()

        # Itera sobre as pessoas e insere
        for pessoa in pessoas:
            cursor.execute(SQL_PESSOA, pessoa.gerar_linha_sql())

        print(f"Escrito {len(pessoas)} pessoa(s).")
        conn.commit()
