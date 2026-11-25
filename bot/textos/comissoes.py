from telebot.formatting import hbold, hcode, hitalic, hlink

from bot.utils import formatar_email
from constantes import CodigosCoCs, CodigosDeptos, NomesDeptos
from entidades.comissao import Chapa, Comissao, MembroComissao
from entidades.pessoa import PessoaICMC


def formatar_str_membro_comissao(membro: PessoaICMC | None) -> str:
    return f"{membro.nome}: {formatar_email(membro.email)}" if membro is not None else "VACANTE"


class TxtComissao:
    def COMISSAO(comissao: Comissao) -> str:

        txt = f"{hbold(f'👥 COMPOSIÇÃO DE {comissao.nome}')}:\n\n"

        # Agrupa os membros pela categoria
        categorias: dict[str, list[MembroComissao]] = {}
        for m in comissao.membros:
            cat = m.categ_colegiado
            if cat not in categorias:  # Se ainda não está no dicionário, adiciona
                categorias[cat] = []
            categorias[cat].append(m)  # Insere o membro na lista

        # Formata o texto pelas categorias
        lista_cats = []
        for cat, membros in categorias.items():
            txt_cat = f"📌 {hbold(cat)}\n"
            for m in membros:
                comeco_txt = "👤 "
                if m.func_colegiado == m.func_membro:
                    txt_func = ""
                elif m.func_colegiado == "Titular":
                    txt_func = "[T] "
                elif m.func_colegiado == "Suplente":
                    txt_func = "[S] "
                    comeco_txt = "              "
                else:
                    txt_func = f"[{hbold(m.func_colegiado)}] "

                txt_cat += f"{comeco_txt}{txt_func}{m.nome}\n"

            lista_cats.append(txt_cat)

        txt += f"{'\n'.join(lista_cats)}\n{
            f'{hitalic('Fonte:')} {hlink(comissao.link, comissao.link)}'
        }"
        return txt

    def COC(coords: dict[str, Chapa], rds: dict[str, MembroComissao]) -> str:
        # Formata os textos
        txt = ""
        for item in CodigosCoCs:
            chapa = coords[item.name]
            representantes = rds[item.name]

            txt_representantes = ""
            for r in representantes:
                txt_func = "[T] " if r.func_colegiado == "Titular" else "[S] "
                txt_representantes += f"{txt_func}{r.nome}\n"

            txt += (
                f"🎓 {hbold(f'CoC-{item.name}')}\n"
                f"[Coord.] {formatar_str_membro_comissao(chapa.pres)}\n"
                f"[Vice] {formatar_str_membro_comissao(chapa.vice)}\n"
                f"{
                    ''
                    if not txt_representantes
                    else f'{hbold('👤 Representantes discentes')}:\n{txt_representantes}'
                }"
                "\n"
            )

        return f"{hbold('COORDENAÇÕES DE CURSOS DO ICMC')}\n\n{txt}"

    def DEPTO(chefias: dict[str, Chapa], rds: dict[str, MembroComissao]) -> str:
        # Formata os textos
        txt = ""
        for item in CodigosDeptos:
            chapa = chefias[item.name]
            representantes = rds[item.name]

            txt_representantes = ""
            for r in representantes:
                txt_func = "[T] " if r.func_colegiado == "Titular" else "[S] "
                txt_representantes += f"{txt_func}{r.nome}\n"

            txt += (
                f"🏫 {hbold(f'Departamento de {NomesDeptos[item.name]}')}\n"
                f"[Chefe] {formatar_str_membro_comissao(chapa.pres)}\n"
                f"[Vice] {formatar_str_membro_comissao(chapa.vice)}\n"
                f"{
                    ''
                    if not txt_representantes
                    else f'{hbold('👤 Representantes discentes')}:\n{txt_representantes}'
                }"
                "\n"
            )

        return f"{hbold('CHEFIAS DE DEPARTAMENTOS DO ICMC')}\n\n{txt}"

    def NAO_ENCONTRADA(nome: str) -> str:
        return f"A comissão {hcode(nome)} não foi encontrada!"

    def COD_NAO_ENCONTRADO(codigo: str, sigla: str) -> str:
        return f"A comissão de código {hcode(codigo)} e sigla {hcode(sigla)} não foi encontrada!"
