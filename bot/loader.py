import asyncio
import re
from datetime import datetime, timedelta
from importlib import import_module
from pathlib import Path

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

import bot.query as query
from bot.entidades.comando import COMANDOS_BOT, COMANDOS_FUNCS
from bot.entidades.mensagem import MSGS_COM_BOTOES_DINAMICOS
from constantes import Caminhos


# Registra os comandos do bot no Telegram
async def registrar_comandos(bot: AsyncTeleBot) -> None:

    # Só de importar os arquivos, os comandos já são registrados
    for arq in Path(Caminhos.PASTA_COMANDOS).rglob("*.py"):
        import_module(Caminhos.CMD(arq.stem))

    # Registra todos os comandos no menu do bot, priorizando os mais úteis
    with open(Caminhos.COMANDOS_UTEIS, encoding="utf-8") as txt:
        comandos_uteis = txt.read().split("\n")
        for c in COMANDOS_BOT:
            if c.command in comandos_uteis:
                c.description = "⭐ " + c.description

        await bot.delete_my_commands()  # Deleta os antigos
        COMANDOS_BOT.sort(key=lambda c: c.command.lower())  # Põe em ordem alfabética
        await bot.set_my_commands(COMANDOS_BOT)  # Define os novos

    # Registra todos os handlers de mensagem
    @bot.message_handler(func=lambda m: m.text and m.text.startswith("/"))
    async def handler_global(mensagem: Message) -> None:

        # Separa o comando em partes e remove itens em branco
        if not (partes := list(filter(lambda s: s, re.split("[_ ]", mensagem.text[1:])))):
            return

        # Obtém as partes do comando
        nome_comando = partes[0].split("@")[0]
        argumentos = partes[1:]
        # Se não é um comando válido
        if nome_comando not in COMANDOS_FUNCS:
            await bot.reply_to(
                mensagem,
                "❌ Comando inválido! Use /help para ver a lista de comandos.",
                parse_mode="HTML",
            )
            return
        # Executa o comando
        await COMANDOS_FUNCS[nome_comando].executar(mensagem, bot, argumentos)


# Remove mensagens com botões dinâmicos após certo tempo
async def remover_mensagens_expiradas() -> None:
    while True:
        limite = datetime.now() - timedelta(days=5)  # 5 dias

        expiradas = [
            chave for chave, msg in MSGS_COM_BOTOES_DINAMICOS.items() if msg.data_criacao <= limite
        ]
        for chave in expiradas:
            del MSGS_COM_BOTOES_DINAMICOS[chave]

        await asyncio.sleep(60 * 60)  # Verifica a cada hora


# Registra os handlers de apertos de botões e outras interações
async def registrar_query_handlers(bot: AsyncTeleBot) -> None:

    # Handler nop
    bot.register_callback_query_handler(
        query.handler_nop, func=lambda c: c.data.startswith("nop"), pass_bot=True
    )

    # Handlers dos botões
    bot.register_callback_query_handler(
        query.handler_menu,
        func=lambda c: c.data.startswith("menu:"),
        pass_bot=True,
    )
    bot.register_callback_query_handler(
        query.handler_res_de_busca,
        func=lambda c: c.data.startswith("pg:"),
        pass_bot=True,
    )
