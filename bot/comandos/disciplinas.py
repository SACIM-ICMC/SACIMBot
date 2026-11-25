from telebot.async_telebot import AsyncTeleBot
from telebot.types import LinkPreviewOptions as LinkPrev
from telebot.types import Message
from telebot.formatting import hbold 

from bot.entidades.callback import CallbackData as CD
from bot.entidades.comando import criar_comando
from bot.entidades.mensagem import MsgDisciplina, MsgListaDeResultados
from bot.entidades.resultados import Resultado
from bot.textos.disciplinas import TxtDisc
from bot.utils import check_args
from db.read.disciplina import (
    buscar_disc_por_codigo,
    buscar_discs_por_nome,
    buscar_oferecimentos_por_codigo_disc,
    buscar_requisitos_por_codigo_disc,
)

from constantes import URLICMC
from scraper.utils import extrair_pagina



@criar_comando(
    nome="disc",
    descricao="Busca uma disciplina pelo código",
    validador=check_args,
    msg_erro="❌ Uso correto do comando: disc [código]",
)
async def disccod(message: Message, bot: AsyncTeleBot, args: list[str]) -> None:

    codigo = args[0].upper()
    # Obtém resultado
    disc = buscar_disc_por_codigo(codigo)

    if not disc:
        txt = TxtDisc.COD_NAO_ENCONTRADO(codigo)
        # Responde a mensagem
        await bot.reply_to(message, txt, parse_mode="HTML")
        return

    # Então manda a mensagem completa, com botões
    requisitos = buscar_requisitos_por_codigo_disc(codigo)
    oferecimentos = buscar_oferecimentos_por_codigo_disc(codigo)
    msg_disc = MsgDisciplina(bot, message.from_user.id, disc, requisitos, oferecimentos)
    await msg_disc.enviar_primeira_mensagem(message)  # Manda a mensagem


@criar_comando(
    nome="nomedisc",
    descricao="Busca uma disciplina pelo nome",
    validador=check_args,
    msg_erro="❌ Uso correto do comando: nomedisc [nome]",
)
async def discnome(msg: Message, bot: AsyncTeleBot, args: list[str]) -> None:

    nome = " ".join(args)  # Nome da disciplina a ser buscada

    # Obtém resultados
    auto_sugerir, res = buscar_discs_por_nome(nome)

    if len(res) == 0:  # Se não encontrou nada
        txt = TxtDisc.NOME_NAO_ENCONTRADO(nome)
        # Responde o bot
        await bot.reply_to(msg, txt, parse_mode="HTML", link_preview_options=LinkPrev(True))
        return

    if auto_sugerir:
        # Caso a busca sugira que um resultado é o mais provável, imprimimos esse resultado
        codigo = res[0]["codigo"]
        requisitos = buscar_requisitos_por_codigo_disc(codigo)
        oferecimentos = buscar_oferecimentos_por_codigo_disc(codigo)
        msg_botoes = MsgDisciplina(bot, msg.from_user.id, res[0], requisitos, oferecimentos)
    else:
        # Lista dos possíveis resultados com paginação
        lista = [Resultado(r.nome, r.codigo, f"({r.codigo}) {r.nome}") for r in res]
        msg_botoes = MsgListaDeResultados(bot, msg.from_user.id, lista, nome, CD.ItemPg.DISCIPLINA)

    await msg_botoes.enviar_primeira_mensagem(msg)  # Manda a mensagem


@criar_comando(
    nome="oferecimento",
    descricao="Retorna o arquivo com o oferecimento de cada matéria de um departamento do ICMC",
    validador=check_args,
    msg_erro="Uso correto do comando: oferecimento [departamento]",
)
async def oferecimento(msg: Message, bot: AsyncTeleBot, args: list[str]) -> None:
    departamento = " ".join(args).upper()

    if departamento not in ['SMA', 'SSC', 'SCC', 'SME']:
        await bot.reply_to (
            msg,
            f"❌ Verifique a sigla do departamento e tente novamente."
        )
        return
    
    soup = extrair_pagina(URLICMC.OFERECIMENTOS_ICMC)

    oferecimento_dpto = []

    for a in soup.select("a"):
        if "Disciplinas de código" in a.text:
            if (link_dpto := a.get("href")) and departamento in a.text.upper():
                oferecimento_dpto.append(link_dpto)
    
    if len(oferecimento_dpto) == 1:
        await bot.reply_to (
            msg,
            f"Disciplinas do departamento {hbold(departamento)} no {hbold('primeiro semestre')}: {oferecimento_dpto[0]}\n\n"
            f"❌ Ainda não foram encontradas disciplinas do segundo semestre.",
            parse_mode = "HTML"
        )
    else:
        await bot.reply_to (
        msg,
        f"Disciplinas do departamento {hbold(departamento)} no {hbold('primeiro semestre')}: {oferecimento_dpto[0]}\n\n"
        f"Disciplinas do departamento {hbold(departamento)} no {hbold('segundo semestre')}: {oferecimento_dpto[1]}",
        parse_mode = "HTML"
    )

