from enum import StrEnum

from telebot.types import InlineKeyboardButton as Button
from telebot.types import InlineKeyboardMarkup as Markup

from bot.entidades.callback import CallbackData as CD
from bot.entidades.menu import Menu
from bot.entidades.resultados import ResDeBusca


# Estilos de botão
class EstiloBotao(StrEnum):
    PRIMARY = "primary"
    DANGER = "danger"
    SUCCESS = "success"


# BOTÕES


# Para o botão de controle
def gerar_botao_ctrl_pg(id_pg: str, tipo: CD.AcaoPg, habilitado: bool = True) -> Button:
    # Texto do botão
    txts = {
        CD.AcaoPg.PRIMEIRA: "⏪",
        CD.AcaoPg.ANTERIOR: "◀️",
        CD.AcaoPg.PROXIMA: "▶️",
        CD.AcaoPg.ULTIMA: "⏩",
    }
    data = CD.pg_ctrl(id_pg, tipo) if habilitado else CD.nop()
    style = EstiloBotao.SUCCESS if habilitado else None
    return Button(text=txts[tipo], style=style, callback_data=data)


# Para o botão de página
def gerar_botao_nro_pg(pg_atual: int, pg_total: int) -> Button:
    return Button(text=f"{pg_atual} / {pg_total}", callback_data=CD.nop())


# Para o item da página
def gerar_botao_item_pg(id_pg: str, id_entidade: str, num_item: int, tipo: CD.ItemPg) -> Button:
    data = CD.pg_item(id_pg, tipo, id_entidade)
    return Button(text=f"[{num_item}]", style=EstiloBotao.PRIMARY, callback_data=data)


# Para o item do menu
def gerar_botao_item_menu(id_menu: str, item_menu: CD.ItemMenu, habilitado: bool = True) -> Button:
    txts = {
        CD.ItemMenu.CAPA_PESSOA: "🏠",
        CD.ItemMenu.HORARIOS: "⏰",
        CD.ItemMenu.CAPA_DISC: "🏠",
        CD.ItemMenu.EMENTA: "📑",
        CD.ItemMenu.AVALIACAO: "💯",
        CD.ItemMenu.BIBLIOGRAFIA: "📚",
        CD.ItemMenu.EXTENSAO: "🫂",
        CD.ItemMenu.CAPA_PESQ: "🏠",
        CD.ItemMenu.LINHAS: "📋",
        CD.ItemMenu.REQUISITOS: "✅",
        CD.ItemMenu.OFERECIMENTOS: "⏰",
    }
    data = CD.menu_item(id_menu, item_menu)
    style = EstiloBotao.SUCCESS if habilitado else None
    return Button(text=txts[item_menu], style=style, callback_data=data)


# BOTÕES ESPECÍFICOS DE MENSAGENS


def gerar_botoes_do_menu(menu: Menu, id_menu: str) -> Markup:
    # Adicina todos os botões na lista
    botoes = []
    for m in menu.lista_menus:
        ativ = menu.menu_atual != m
        botoes.append(gerar_botao_item_menu(id_menu, m, ativ))
    # Adiciona a lista no keyboard
    keyboard = Markup().row(*botoes)
    return keyboard


def gerar_botoes_da_msg_lista(
    res: ResDeBusca,
    id_pg: str,
    tipo_res: CD.ItemPg,
) -> Markup:

    keyboard = Markup()
    # Adiciona se tem mais de uma pagina
    if res.nro_pgs != 1:
        ativ = res.pg_atual > 0
        b1 = gerar_botao_ctrl_pg(id_pg, CD.AcaoPg.PRIMEIRA, ativ)
        b2 = gerar_botao_ctrl_pg(id_pg, CD.AcaoPg.ANTERIOR, ativ)
        b3 = gerar_botao_nro_pg(res.pg_atual + 1, res.nro_pgs)  # Botão da paginação
        ativ = res.pg_atual < res.nro_pgs - 1
        b4 = gerar_botao_ctrl_pg(id_pg, CD.AcaoPg.PROXIMA, ativ)
        b5 = gerar_botao_ctrl_pg(id_pg, CD.AcaoPg.ULTIMA, ativ)
        # Adiciona todos
        keyboard.row(b1, b2, b3, b4, b5)

    # Adiciona os resultados nos menus
    botoes_itens = []
    for i in range(res.inicio, res.fim):
        botoes_itens.append(gerar_botao_item_pg(id_pg, res.lista[i].id_item, i + 1, tipo_res))
    keyboard.row(*botoes_itens)

    return keyboard
