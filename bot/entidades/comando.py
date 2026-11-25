from collections.abc import Callable
from dataclasses import dataclass

from telebot.async_telebot import AsyncTeleBot
from telebot.types import BotCommand, LinkPreviewOptions, Message

COMANDOS_BOT: list[BotCommand] = []  # Lista de BotCommand para serem adicionados ao bot
COMANDOS_FUNCS: dict[str, "Comando"] = {}  # Dicionário de funções


# Classe comando
@dataclass
class Comando:
    validador: Callable[[list[str]], None] | None = None  # Validador
    msg_estatica: str | None = None  # Se o comando só precisa mandar uma mensagem
    msg_erro: str | None = None  # Mensagem de erro a ser mandada pelo validador
    cmd: Callable[[list[str]], None] | None = None  # Lógica do comando

    # Execução do comando
    async def executar(self, msg: Message, bot: AsyncTeleBot, args: list[str]) -> None:

        # Se não passar no validador, manda a mensagem de erro
        if self.validador and not self.validador(args):
            await bot.reply_to(msg, self.msg_erro, parse_mode="HTML")
            return

        # Se a função for estática: só precisa mandar uma mensagem
        if self.msg_estatica:
            await bot.reply_to(
                msg,
                self.msg_estatica,
                parse_mode="HTML",
                link_preview_options=LinkPreviewOptions(True),
            )
            return

        # Executa a função propriamente dita
        await self.cmd(msg, bot, args)


# Função para inserir um comando no bot
def inserir_comando_no_bot(nome: str, desc: str) -> None:
    # Insere na lista de comandos do bot
    COMANDOS_BOT.append(BotCommand(nome, desc))


# Função para inserir um comando no dicionario
def inserir_comando_nas_funcs(comando: Comando, nome: str, alias: list[str] | None) -> None:
    # Insere no dicionário de funções
    COMANDOS_FUNCS[nome] = comando
    if alias is not None:
        for a in alias:
            COMANDOS_FUNCS[a] = comando


# Função para criar um comando
def criar_comando(
    nome: str,  # Nome do comando
    descricao: str | None = None,  # Descrição do comando a aparecer no menu do bot
    alias: list[str] | None = None,  # Lista de comandos equivalentes
    validador: Callable[[list[str]], None] | None = None,
    msg_estatica: str | None = None,
    msg_erro: str | None = None,
) -> Callable[[Callable[..., None]], Callable[..., None]]:
    # Se o comando tiver uma mensagem estática
    if msg_estatica:
        c = Comando(msg_estatica=msg_estatica)
        # Adiciona o comando
        inserir_comando_no_bot(nome, descricao)
        inserir_comando_nas_funcs(c, nome, alias)

    # Decorador da função
    def decorador(funcao: Callable[[list[str]], None]) -> Callable[[list[str]], None]:
        c = Comando(validador=validador, msg_erro=msg_erro, cmd=funcao)
        # Adiciona o comando
        inserir_comando_no_bot(nome, descricao)
        inserir_comando_nas_funcs(c, nome, alias)

        return funcao

    return decorador
