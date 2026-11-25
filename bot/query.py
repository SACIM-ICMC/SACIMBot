from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery
from telebot.types import EphemeralMessageParameters as Eph
from telebot.types import LinkPreviewOptions as LinkPrev

from bot.entidades.callback import CallbackData as CD
from bot.entidades.mensagem import (
    MSGS_COM_BOTOES_DINAMICOS,
    MsgComBotoesDinamicos,
    MsgDisciplina,
    MsgPesquisa,
    MsgPessoa,
)
from bot.textos.comissoes import TxtComissao
from bot.textos.disciplinas import TxtDisc
from bot.textos.pesquisas import TxtPesquisa
from bot.textos.pessoas import TxtPessoa
from bot.textos.utils import MSG_EXPIRADA, MSG_USUARIO_INVALIDO
from db.read.comissao import buscar_comissao_por_cod_e_sigla
from db.read.disciplina import (
    buscar_disc_por_codigo,
    buscar_horarios_por_nome_prof,
    buscar_oferecimentos_por_codigo_disc,
    buscar_requisitos_por_codigo_disc,
)
from db.read.pesquisa import buscar_pesquisa_por_id, buscar_pesquisas_por_id_pessoa
from db.read.pessoa import buscar_pessoa_por_id


# Valida se um clique de botão é válido
async def validar_interacao(
    call: CallbackQuery, bot: AsyncTeleBot, id_msg: int
) -> MsgComBotoesDinamicos | None:
    msg = MSGS_COM_BOTOES_DINAMICOS.get(id_msg)

    # Se a mensagem não é válida mais
    if not msg:
        await bot.send_message(
            call.message.chat.id,
            MSG_EXPIRADA,
            ephemeral_message_parameters=Eph(
                receiver_user_id=call.from_user.id,
                callback_query_id=call.id,
            ),
        )
        return None

    # Se não foi o mesmo usuário que criou o menu, avisa
    if call.from_user.id != msg.id_usuario:
        await bot.send_message(
            call.message.chat.id,
            MSG_USUARIO_INVALIDO,
            ephemeral_message_parameters=Eph(
                receiver_user_id=call.from_user.id,
                callback_query_id=call.id,
            ),
        )
        return None
    return msg


async def handler_nop(call: CallbackQuery, bot: AsyncTeleBot) -> None:
    # Responde temporariamente o callback
    await bot.answer_callback_query(call.id)


async def handler_menu(call: CallbackQuery, bot: AsyncTeleBot) -> None:
    # Responde temporariamente o callback
    await bot.answer_callback_query(call.id)

    id_menu, item_menu, _ = CD.parse(call.data)

    msg_menu = await validar_interacao(call, bot, id_menu)
    if not msg_menu:
        return

    await msg_menu.executar_acao(CD.ItemMenu(item_menu))


async def handler_res_de_busca(call: CallbackQuery, bot: AsyncTeleBot) -> None:
    # Responde temporariamente o callback
    await bot.answer_callback_query(call.id)

    id_chat = call.message.chat.id
    id_pg, cod, id_entidade = CD.parse(call.data)

    msg_lista = await validar_interacao(call, bot, id_pg)
    if not msg_lista:
        return

    # Clique em controle de página
    if CD.pertence(CD.AcaoPg, cod):
        await msg_lista.executar_acao(CD.AcaoPg(cod))
        return
    # Clique em opção
    if CD.pertence(CD.ItemPg, cod):
        await msg_lista.finalizar()

        funcs = {
            CD.ItemPg.PESSOA: enviar_mensagem_da_pessoa_pelo_id,
            CD.ItemPg.PESQUISA: enviar_mensagem_da_pesquisa_pelo_id,
            CD.ItemPg.DISCIPLINA: enviar_mensagem_da_disciplina_pelo_codigo,
            CD.ItemPg.COMISSAO: enviar_mensagem_da_comissao_pelo_cod_e_sigla,
        }
        await funcs[CD.ItemPg(cod)](msg_lista.id_usuario, id_chat, bot, id_entidade)


async def enviar_mensagem_da_pessoa_pelo_id(
    id_usuario: int, id_chat: int, bot: AsyncTeleBot, id_pessoa: str
) -> None:
    # Efetua a busca
    pessoa = buscar_pessoa_por_id(id_pessoa)
    if not pessoa:
        txt = TxtPessoa.ID_NAO_ENCONTRADO(id_pessoa)
        await bot.send_message(id_chat, txt, parse_mode="HTML", link_preview_options=LinkPrev(True))
        return

    pesquisas = buscar_pesquisas_por_id_pessoa(id_pessoa)
    horarios = buscar_horarios_por_nome_prof(pessoa.nome)
    # Mensagem do menu
    msg_botoes = MsgPessoa(bot, id_usuario, pessoa, pesquisas, horarios)
    await msg_botoes.enviar_primeira_mensagem(id_chat)


async def enviar_mensagem_da_pesquisa_pelo_id(
    id_usuario: int, id_chat: int, bot: AsyncTeleBot, id_pesquisa: str
) -> None:
    # Efetua a busca
    pesquisa = buscar_pesquisa_por_id(id_pesquisa)
    if not pesquisa:
        txt = TxtPesquisa.ID_NAO_ENCONTRADO(id_pesquisa)
        await bot.send_message(id_chat, txt, parse_mode="HTML", link_preview_options=LinkPrev(True))
        return

    # Mensagem do menu
    msg_botoes = MsgPesquisa(bot, id_usuario, pesquisa)
    await msg_botoes.enviar_primeira_mensagem(id_chat)


async def enviar_mensagem_da_disciplina_pelo_codigo(
    id_usuario: int, id_chat: int, bot: AsyncTeleBot, cod_disc: str
) -> None:
    # Efetua a busca
    disc = buscar_disc_por_codigo(cod_disc)
    if not disc:
        txt = TxtDisc.COD_NAO_ENCONTRADO(cod_disc)
        await bot.send_message(id_chat, txt, parse_mode="HTML", link_preview_options=LinkPrev(True))
        return

    requisitos = buscar_requisitos_por_codigo_disc(cod_disc)
    oferecimentos = buscar_oferecimentos_por_codigo_disc(cod_disc)
    msg_botoes = MsgDisciplina(bot, id_usuario, disc, requisitos, oferecimentos)
    await msg_botoes.enviar_primeira_mensagem(id_chat)


async def enviar_mensagem_da_comissao_pelo_cod_e_sigla(
    id_usuario: int, id_chat: int, bot: AsyncTeleBot, cod_com: str
) -> None:
    # Parsa a identificação
    codigo, sigla = cod_com.split("-")
    # Efetua a busca
    comissao = buscar_comissao_por_cod_e_sigla(codigo, sigla)
    if comissao:
        txt = TxtComissao.COMISSAO(comissao)
    else:
        txt = TxtComissao.COD_NAO_ENCONTRADO(codigo, sigla)

    await bot.send_message(id_chat, txt, parse_mode="HTML", link_preview_options=LinkPrev(True))
