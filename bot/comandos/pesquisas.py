from telebot.async_telebot import AsyncTeleBot
from telebot.types import LinkPreviewOptions as LinkPrev
from telebot.types import Message

from bot.entidades.callback import CallbackData as CD
from bot.entidades.comando import criar_comando
from bot.entidades.mensagem import MsgListaDeResultados, MsgPesquisa
from bot.entidades.resultados import Resultado
from bot.textos.pesquisas import TxtPesquisa
from bot.utils import check_args
from db.read.pesquisa import buscar_pesquisas_por_nome


@criar_comando(
    nome="pesquisa",
    descricao="Pesquisas do ICMC",
    validador=check_args,
    msg_erro="❌ Uso correto do comando: pesquisa [área de pesquisa]",
)
async def pesquisa(msg: Message, bot: AsyncTeleBot, args: list[str]) -> None:

    nome = " ".join(args)  # Nome da pesquisa a ser buscada

    # Obtém resultados
    auto_sugerir, pesquisas = buscar_pesquisas_por_nome(nome)

    if len(pesquisas) == 0:  # Se não encontrou nada
        txt = TxtPesquisa.NAO_ENCONTRADA(nome)
        await bot.reply_to(msg, txt, parse_mode="HTML", link_preview_options=LinkPrev(True))
        return

    if auto_sugerir:
        # Caso a busca sugira que um resultado é o mais provável, imprimimos esse resultado
        msg_botoes = MsgPesquisa(bot, msg.from_user.id, pesquisas[0])
    else:
        # Então mostramos um menu de paginação com os possíveis resultados
        lista = [Resultado(pesq.nome, pesq.id_site) for pesq in pesquisas]
        msg_botoes = MsgListaDeResultados(bot, msg.from_user.id, lista, nome, CD.ItemPg.PESQUISA)
    await msg_botoes.enviar_primeira_mensagem(msg)  # Manda a mensagem
