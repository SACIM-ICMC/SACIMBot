from telebot.async_telebot import AsyncTeleBot
from telebot.types import LinkPreviewOptions as LinkPrev
from telebot.types import Message

from bot.entidades.callback import CallbackData as CD
from bot.entidades.comando import criar_comando
from bot.entidades.mensagem import MsgListaDeResultados, MsgPessoa
from bot.entidades.resultados import Resultado
from bot.textos.pessoas import TxtEmail, TxtPessoa, TxtSala
from bot.utils import check_args
from db.read.disciplina import buscar_horarios_por_nome_prof
from db.read.pesquisa import buscar_pesquisas_por_id_pessoa
from db.read.pessoa import buscar_pessoas_por_nome


@criar_comando(
    nome="email",
    descricao="Qual é o email do(a)?",
    validador=check_args,
    msg_erro="❌ Uso correto do comando: email [nome da pessoa]",
)
async def email(msg: Message, bot: AsyncTeleBot, args: list[str]) -> None:

    nome = " ".join(args)  # Nome da pessoa

    # Obtém resultados
    auto_sugerir, pessoas = buscar_pessoas_por_nome(nome)

    if len(pessoas) == 0:  # Se não encontrou nada
        txt = TxtPessoa.NAO_ENCONTRADA(nome)
    elif auto_sugerir:
        # Caso a busca sugira que um resultado é o mais provável, imprimimos esse resultado
        txt = TxtEmail.EMAIL(pessoas[0].nome, pessoas[0].email)
    else:  #  Então mostramos uma lista dos possíveis resultados
        lista = ((p.nome, p.email) for p in pessoas)
        txt = TxtEmail.LISTAR(nome, len(pessoas), lista)

    await bot.reply_to(msg, txt, parse_mode="HTML")


@criar_comando(
    nome="pessoa",
    descricao="Informações do icmc/pessoas",
    validador=check_args,
    msg_erro="❌ Uso correto do comando: pessoa [nome da pessoa]",
)
async def pessoa(msg: Message, bot: AsyncTeleBot, args: list[str]) -> None:

    nome = " ".join(args)  # Nome da pessoa a ser buscada

    # Obtém resultados
    auto_sugerir, pessoas = buscar_pessoas_por_nome(nome)

    if len(pessoas) == 0:  # Se não encontrou nada
        txt = TxtPessoa.NAO_ENCONTRADA(nome)
        # Responde o bot
        await bot.reply_to(msg, txt, parse_mode="HTML", link_preview_options=LinkPrev(True))
        return

    if auto_sugerir:
        # Caso a busca sugira que um resultado é o mais provável, imprimimos esse resultado
        pesquisas = buscar_pesquisas_por_id_pessoa(pessoas[0].id_site)
        horarios = buscar_horarios_por_nome_prof(pessoas[0].nome)
        # Mensagem do menu
        msg_botoes = MsgPessoa(bot, msg.from_user.id, pessoas[0], pesquisas, horarios)
    else:
        # Lista dos possíveis resultados com paginação
        lista = [Resultado(p.nome, p.id_site) for p in pessoas]
        msg_botoes = MsgListaDeResultados(bot, msg.from_user.id, lista, nome, CD.ItemPg.PESSOA)

    await msg_botoes.enviar_primeira_mensagem(msg)  # Manda a mensagem


@criar_comando(
    nome="sala",
    descricao="Alguém sabe onde é a sala do(a)?",
    validador=check_args,
    msg_erro="❌ Uso correto do comando: sala [nome da pessoa]",
)
async def sala(msg: Message, bot: AsyncTeleBot, args: list[str]) -> None:

    nome = " ".join(args)  # Nome da pessoa a ser buscada

    # Realiza a busca
    auto_sugerir, pessoas = buscar_pessoas_por_nome(nome)

    if len(pessoas) == 0:  # Se não encontrou nada
        txt = TxtPessoa.NAO_ENCONTRADA(nome)
    elif auto_sugerir:
        # Caso a busca sugira que um resultado é o mais provável, imprimimos esse resultado
        txt = TxtSala.SALA(pessoas[0].nome, pessoas[0].sala)
    else:  # Então mostramos uma lista dos possíveis resultados
        lista = ((p.nome, p.sala) for p in pessoas)
        txt = TxtSala.LISTAR(nome, len(pessoas), lista)

    await bot.reply_to(msg, txt, parse_mode="HTML")
