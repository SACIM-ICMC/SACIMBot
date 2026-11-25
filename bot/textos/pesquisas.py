from telebot.formatting import hbold, hcode, hitalic, hlink

from constantes import URLICMC
from entidades.pesquisa import Pesquisa


class TxtPesquisa:
    def NAO_ENCONTRADA(nome: str) -> str:
        return f"A pesquisa {hcode(nome)} não foi encontrada!"

    def ID_NAO_ENCONTRADO(id: str) -> str:
        return f"A pesquisa de ID {hcode(id)} não foi encontrada!"

    def PESQUISA(pesquisa: Pesquisa) -> str:
        filtro_labs = [lab for lab in pesquisa.labs if lab.nome and lab.link]
        txt_labs = ""
        if filtro_labs:
            txt_labs = f"{hbold('Laboratórios:')}\n{'\n'.join(f'- {hlink(lab.nome, lab.link)}' for lab in filtro_labs)}\n\n"

        return (
            f"{hbold(pesquisa.nome)}\n"
            f"{hitalic(pesquisa.area)}\n"
            "\n"
            f"{txt_labs}"
            f"{hbold('Docentes:')}\n"
            f"{'\n'.join([d.nome for d in pesquisa.docentes])}\n"
            "\n"
            f"{f'{hitalic('Fonte:')} {hlink(URLICMC.PESQUISA(pesquisa.id_site), URLICMC.PESQUISA(pesquisa.id_site))}'}\n"
        )

    def LINHAS(nome_pesq: str, linhas: list[str]) -> str:
        txt_header = f"📋 {hbold(f'Linhas de pesquisa de "{nome_pesq}"')}:\n"
        txt_linhas = "\n".join([f"- {linha}" for linha in linhas])
        return f"{txt_header}\n{txt_linhas}\n"
