from telebot.formatting import escape_html as scp
from telebot.formatting import hbold, hcode, hitalic

from constantes import DIAS
from entidades.disciplina import Disciplina
from entidades.oferecimento import Oferecimento
from entidades.requisito import Requisito


class TxtDisc:
    def NOME_NAO_ENCONTRADO(nome: str) -> str:
        return f"A disciplina de nome {hcode(nome)} não foi encontrada!"

    def COD_NAO_ENCONTRADO(codigo: str) -> str:
        return f"A disciplina de código {hcode(codigo)} não foi encontrada!"

    def DISC(disc: Disciplina) -> str:
        return (
            f"{disc.unidade}\n"
            f"{hbold('Departamento')}: {disc.departamento}\n"
            "\n"
            f"Disciplina: {hbold(disc.codigo) + ' - ' + disc.nome}\n"
            f"{hitalic(disc.nome_ingles)}\n"
            "\n"
            f"{hbold('Créditos Aula:')} {disc.creditos_aula or 0}\n"
            f"{hbold('Créditos Trabalho:')} {disc.creditos_trab or 0}\n"
            f"{hbold('Carga Horária Total:')} {disc.carga_horaria or 0}h\n"
            f"{hbold('Carga Horária Extensão:')} {disc.carga_horaria_extensao or 0}h\n"
            f"{hbold('Tipo:')} {disc.tipo}\n"
            f"{hbold('Ativação:')} {disc.data_ativacao}\n"
            f"{'' if not disc.data_desativacao else f'{hbold('Desativação:')} {disc.data_desativacao}\n'}"
            f"{
                ''
                if not disc.docentes_responsaveis
                else f'\n{hbold('Docentes Responsáveis:')}\n{scp('\n'.join([f"{p.nusp} - {p.nome}" for p in disc.docentes_responsaveis]))}\n'
            }"
        )

    def EMENTA(disc: Disciplina) -> str:
        return (
            f"{hbold('Ementa:')}\n"
            f"{scp(disc.ementa)}\n"
            "\n"
            f"{hbold('Objetivos:')}\n"
            f"{scp(disc.objetivos)}\n"
            "\n"
            f"{hbold('Conteúdo Programático:')}\n"
            f"{scp(disc.conteudo)}\n"
        )

    def AVALIACAO(disc: Disciplina) -> str:
        return (
            f"{hbold('Instrumentos e Critérios de Avaliação')}\n"
            f"{hbold('Método de Avaliação')}\n"
            f"{scp(disc.metodo_avaliacao)}\n"
            "\n"
            f"{hbold('Critério de Avaliação')}\n"
            f"{scp(disc.criterios_avaliacao)}\n"
            "\n"
            f"{hbold('Norma de Recuperação')}\n"
            f"{scp(disc.recuperacao)}\n"
        )

    def BIBLIOGRAFIA(disc: Disciplina) -> str:
        return f"{hbold('Bibliografia')}\n{scp(disc.bibliografia)}\n"

    def EXTENSAO(disc: Disciplina) -> str:
        return f"{
            ''
            if not disc.grupos_ext
            else (
                f'{hbold('Atividades de Extensão')}\n'
                f'{hbold('Grupo social alvo da atividade')}\n'
                f'{scp(disc.grupos_ext)}\n'
                '\n'
                f'{hbold('Objetivos da atividade')}\n'
                f'{scp(disc.objetivos_ext)}\n'
                '\n'
                f'{hbold('Descrição da atividade')}\n'
                f'{scp(disc.descricao_ext)}\n'
                '\n'
                f'{hbold('Indicadores de avaliação da atividade')}\n'
                f'{scp(disc.indicadores_ext)}\n'
                '\n'
            )
        }"

    def REQUISITOS(cod: str, nome: str, reqs: list[Requisito]) -> str:
        if not reqs:
            return f"❌ A disciplina {hbold(f'({cod}) {nome}')} não possui requisitos!\n"

        # Agrupa os requisitos pelo curso
        reqs_por_curso = {}
        for req in reqs:
            c = req.codigo_curso
            # Cria a chave no dicionário se não houver
            if c not in reqs_por_curso:
                reqs_por_curso[c] = {"nome": req.nome_curso, "lista": []}
            # Insere na lista
            reqs_por_curso[c]["lista"].append(req)

        # Formatações
        txt_reqs = f"{hbold(f'REQUISITOS DE {f'({cod}) {nome}'}')}\n\n"
        lista_reqs = []
        for key, value in reqs_por_curso.items():
            txt = f"🎓 {hbold('Curso')}: {key} {value['nome']}:\n"

            id_grupo = 0
            for req in value["lista"]:
                # Se mudou o id_grupo, atualiza e adiciona "OU"
                if req.id_grupo != id_grupo:
                    txt += f"{hbold('OU')}\n"
                    id_grupo = req.id_grupo
                # Adiciona o requisito à lista
                txt += f"📌 {hbold(f'{req.codigo_requisito} {req.nome_requisito}')}\n({req.tipo}) - Período ideal: {req.periodo_ideal}\n"

            lista_reqs.append(txt)

        return txt_reqs + "\n".join(lista_reqs)

    def OFERECIMENTOS(cod: str, nome: str, ofcs: list[Oferecimento]) -> str:
        if not ofcs:
            return f"❌ A disciplina {hbold(f'({cod}) {nome}')} não possui oferecimentos!\n"

        # Formatações
        txt_ofcs = f"{hbold(f'OFERECIMENTOS DE {f'({cod}) {nome}'}')}\n\n"
        lista_ofcs = []
        for of in ofcs:
            txt = (
                f"📌 {of.codigo_turma}{f' {of.obs_turma}' if of.obs_turma else ''} - {of.tipo}\n"
                f"{f'{hitalic(of.obs)}\n' if of.obs else ''}"
                f"📆 {hbold('Início')}: {of.inicio} {hbold('Fim')}: {of.fim}\n"
            )

            if of.horarios:
                txt += f"⏱️ {hbold('HORÁRIOS')}:\n"
            for h in of.horarios:
                profs = ", ".join(
                    [f"{f'({p.tipo}) ' if p.tipo else ''}{p.nome}" for p in h.professores]
                )
                txt += f"- {DIAS.get(h.dia)}, {h.horario_inicio} às {h.horario_termino}{f' - {profs}' if profs else ''}\n"

            if of.atividades:
                txt += f"⚒️ {hbold('ATIVIDADES')}:\n"
            for a in of.atividades:
                prof = f"{f'({a.tipo}) ' if a.tipo else ''}{a.nome}"
                txt += (
                    f"- {prof} - {a.tipo_atividade}. {hbold('Carga Horária')}: {a.carga_horaria}h\n"
                )

            lista_ofcs.append(txt)

        return txt_ofcs + "\n".join(lista_ofcs)
