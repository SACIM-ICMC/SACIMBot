from typing import TypedDict

from telebot.formatting import hbold, hcode, hitalic, hlink

from bot.utils import formatar_email
from constantes import DIAS, MAX_RESULTADOS, URLICMC
from entidades.oferecimento import Horario, HorarioOfcProfessor
from entidades.pessoa import PessoaICMC


class HorariosPorDisc(TypedDict):
    nome: str
    obs: str
    lista: list[Horario]


class TxtEmail:
    def EMAIL(nome: str, email: str) -> str:
        txt_email = hitalic("Não possui") if not email else formatar_email(email)
        return f"✉️ E-mail de {hbold(nome)}: {txt_email}"

    def LISTAR(busca: str, total: int, lista: list[tuple[str | None]]) -> str:
        if total > MAX_RESULTADOS:
            txt_header = f"Sua busca {hcode(busca)} retornou {hbold(str(total))} pessoas. Tente restringi-la da próxima vez.\nAqui estão as {MAX_RESULTADOS} mais prováveis:\n"
        else:
            txt_header = f"Sua busca {hcode(busca)} retornou {hbold(str(total))} pessoas:\n"
        lista_formatada = [
            f"✉️ E-mail de {hbold(nome)}: {
                hitalic('Não possui') if not email else formatar_email(email)
            }"
            for nome, email in lista
        ]
        lista_formatada = lista_formatada[:MAX_RESULTADOS]

        return f"{txt_header}\n{'\n'.join(lista_formatada)}"


class TxtPessoa:
    def PESSOA(pessoa: PessoaICMC, pesquisas: list[str]) -> str:
        return (
            f"{pessoa.profissao}: {hbold(pessoa.nome)}\n"
            f"{'' if not pessoa.categorias else hitalic('\n'.join(pessoa.categorias)) + '\n'}"
            "\n"
            f"{'' if not pessoa.email else f'✉️ {hbold("E-mail:")} {formatar_email(pessoa.email)}\n'}"
            f"{'' if not pessoa.sala else f'🏠 {hbold("Sala:")} {hcode(pessoa.sala)}\n'}"
            f"{'' if not pessoa.pagina else f'🌐 {hbold("Página pessoal:")} {hlink(pessoa.pagina, pessoa.pagina)}\n'}"
            f"{'' if not pessoa.telefone else f'☎️ {hbold("Telefone:")} {hcode(pessoa.telefone)}\n'}"
            f"{'' if not pessoa.researcher_id else f'🧑‍🔬 {hbold("ResearcherID:")} {hlink(pessoa.researcher_id, URLICMC.RESEARCHER_ID(pessoa.researcher_id))}\n'}"
            f"{'' if not pessoa.lattes else f'📑 {hbold("Currículo Lattes:")} {hlink("Aqui", pessoa.lattes)}\n'}"
            f"{'' if not pessoa.grupos_cnpq else f'👥 {hbold("Grupos CNPq:")} {hlink("Aqui", pessoa.grupos_cnpq)}\n'}"
            "\n"
            f"{'' if not pesquisas else f'👨‍🔬 {hbold('Áreas de pesquisas:')}\n{'\n'.join(pesquisas)}\n\n'}"
            f"{f'{hitalic('Fonte:')} {hlink(URLICMC.PESSOA(pessoa.id_site), URLICMC.PESSOA(pessoa.id_site))}'}\n"
        )

    def HORARIOS(pessoa: str, horarios: list[HorarioOfcProfessor]) -> str:
        if not horarios:
            return f"❌ A pessoa {hbold(pessoa)} não ministra aulas de GRADUAÇÃO nesse semestre!\n"

        # Agrupa os horários por turmas
        horarios_por_disc: dict[str, HorariosPorDisc] = {}
        for h in horarios:
            chave = f"{h.cod_disc}-{h.cod_turma}"
            # Cria a chave no dicionário se não houver
            if chave not in horarios_por_disc:
                horarios_por_disc[chave] = {"nome": h.nome, "obs": h.obs, "lista": []}
            # Insere na lista
            horarios_por_disc[chave]["lista"].append(h.horario)

        # Formatações
        txt_discs = []
        for codigos, disc in horarios_por_disc.items():
            txt = f"📌 {hbold(f'{codigos} {disc['nome']}')}\n{hitalic(disc['obs'])}\n"
            for h in disc["lista"]:
                txt += f"⏱️ {DIAS.get(h.dia)}, {h.horario_inicio} às {h.horario_termino}\n"
            txt_discs.append(txt)

        return (
            f"{hbold(f'⏰ Horários de aula de GRADUAÇÃO de {pessoa}')}:\n\n{'\n'.join(txt_discs)}"
        )

    def NAO_ENCONTRADA(nome: str) -> str:
        return f"A pessoa {hcode(nome)} não foi encontrada!"

    def ID_NAO_ENCONTRADO(id: str) -> str:
        return f"A pessoa de ID {hcode(id)} não foi encontrada!"


class TxtSala:
    def SALA(nome: str, sala: str | None) -> str:
        return f"🏠 Sala de {hbold(nome)}: {hcode(sala) if sala else hitalic('Não possui')}"

    def LISTAR(busca: str, total: int, lista: list[tuple[str | None]]) -> str:
        if total > MAX_RESULTADOS:
            txt_header = f"Sua busca {hcode(busca)} retornou {hbold(str(total))} pessoas. Tente restringi-la da próxima vez.\nAqui estão as {MAX_RESULTADOS} mais prováveis:\n"
        else:
            txt_header = f"Sua busca {hcode(busca)} retornou {hbold(str(total))} pessoas:\n"
        lista_formatada = [
            f"🏠 Sala de {hbold(nome)}: {hcode(sala) if sala else hitalic('Não possui')}"
            for nome, sala in lista
        ]
        lista_formatada = lista_formatada[:MAX_RESULTADOS]

        return f"{txt_header}\n{'\n'.join(lista_formatada)}"

    def NAO_ENCONTRADA(sala: str) -> str:
        return f"🏠 A sala {hcode(sala)} não é de ninguém!"
