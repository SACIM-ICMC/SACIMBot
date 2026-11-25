from telebot.formatting import hbold, hcode

from bot.entidades.resultados import ResDeBusca


class TxtResDeBusca:
    def LISTA(res: ResDeBusca, termo_buscado: str, nome_entidade_plural: str) -> str:
        txt_lista = ""
        for i in range(res.inicio, res.fim):
            txt_lista += f"{hcode(f'[{i + 1}]')} {hbold(res.lista[i].nome_item)}\n"

        return (
            f"Sua busca {hcode(termo_buscado)} retornou {hbold(str(len(res.lista)))} {nome_entidade_plural}.\n"
            f"Mostrando página {res.pg_atual + 1} de {res.nro_pgs}:\n\n"
            f"{txt_lista}\n"
            f"{'' if res.nro_pgs == 1 else 'Navegue pelas páginas pelo menu abaixo.'}"
        )
