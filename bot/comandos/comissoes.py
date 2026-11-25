from telebot.async_telebot import AsyncTeleBot
from telebot.types import LinkPreviewOptions as LinkPrev
from telebot.types import Message

from bot.entidades.callback import CallbackData as CD
from bot.entidades.comando import criar_comando
from bot.entidades.mensagem import MsgListaDeResultados
from bot.entidades.resultados import Resultado
from bot.textos.comissoes import TxtComissao
from bot.utils import check_args
from constantes import CodigosCoCs, CodigosDeptos, SiglasComissoes
from db.read.comissao import (
    buscar_comissoes_por_nome,
    obter_presidencia_por_cod_e_sigla,
    obter_representantes_discentes,
)


@criar_comando(
    nome="comissao",
    descricao="Mandatos de uma comissão",
    validador=check_args,
    msg_erro="❌ Uso correto do comando: comissao [nome]",
)
async def comissao(msg: Message, bot: AsyncTeleBot, args: list[str]) -> None:

    nome = " ".join(args)  # Nome da comissão a ser buscada

    # Obtém resultados
    auto_sugerir, comissoes = buscar_comissoes_por_nome(nome)

    if auto_sugerir or len(comissoes) == 0:
        txt = (
            TxtComissao.COMISSAO(comissoes[0]) if auto_sugerir else TxtComissao.NAO_ENCONTRADA(nome)
        )
        # Responde o bot
        await bot.reply_to(msg, txt, parse_mode="HTML", link_preview_options=LinkPrev(True))
        return

    # Lista dos possíveis resultados com paginação
    lista = [Resultado(comiss.nome, f"{comiss.codigo}-{comiss.sigla}") for comiss in comissoes]
    msg_botoes = MsgListaDeResultados(bot, msg.from_user.id, lista, nome, CD.ItemPg.COMISSAO)

    await msg_botoes.enviar_primeira_mensagem(msg)  # Manda a mensagem


@criar_comando(nome="coc", descricao="Coordenações de Curso")
async def coc(msg: Message, bot: AsyncTeleBot, args: list[str]) -> None:
    # Obtém as coordenações e os RDs
    cocs = {}
    rds = {}
    for item in CodigosCoCs:
        cocs[item.name] = obter_presidencia_por_cod_e_sigla(item.value, SiglasComissoes.COC)
        rds[item.name] = obter_representantes_discentes(item.value, SiglasComissoes.COC)
    # Monta o texto
    txt = TxtComissao.COC(cocs, rds)
    # Responde o bot
    await bot.reply_to(msg, txt, parse_mode="HTML")


@criar_comando(nome="depto", descricao="Departamentos")
async def depto(msg: Message, bot: AsyncTeleBot, args: list[str]) -> None:
    # Obtém as chefias
    deptos = {}
    rds = {}
    for item in CodigosDeptos:
        deptos[item.name] = obter_presidencia_por_cod_e_sigla(item.value, SiglasComissoes.DEPTO)
        rds[item.name] = obter_representantes_discentes(item.value, SiglasComissoes.DEPTO)
    # Monta o texto
    txt = TxtComissao.DEPTO(deptos, rds)
    # Responde o bot
    await bot.reply_to(msg, txt, parse_mode="HTML")
