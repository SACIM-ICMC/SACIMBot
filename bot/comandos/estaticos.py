import json

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from bot.entidades.comando import criar_comando
from bot.textos.estaticos import TxtArquivos, TxtInfos, TxtSACIM
from constantes import Caminhos
from entidades.changelog import Versao

criar_comando("biblio", "Sobre a Biblioteca Achille Bassi", msg_estatica=TxtInfos.BIBLIO)
criar_comando("cartilha", "Cartilhas SACIM 2026", msg_estatica=TxtInfos.CARTILHAS)
criar_comando("eduroam", "Como configurar a eduroam", msg_estatica=TxtInfos.EDUROAM)
criar_comando("grad", "Serviço de Graduação", msg_estatica=TxtInfos.GRAD)
criar_comando("hino", "Hino do CAASO", msg_estatica=TxtSACIM.HINO)
criar_comando("invites", "Links de grupos do Telegram", ["invite"], msg_estatica=TxtSACIM.INVITES)
criar_comando("museu", "Sobre o Museu de Computação", msg_estatica=TxtInfos.MUSEU)
criar_comando("printer", "Como imprimir na Pró-Aluno", msg_estatica=TxtInfos.PRINTER)
criar_comando("redes", "Redes da SACIM", msg_estatica=TxtSACIM.REDES)
criar_comando("repo", "Repositório do Bot", ["github"], msg_estatica=TxtSACIM.REPO)
criar_comando("reservas", "Como reservar salas", msg_estatica=TxtInfos.RESERVAS)
criar_comando("vpn", "Como configurar a VPN USP", msg_estatica=TxtInfos.VPN)


@criar_comando("versoes", "Versões do Bot", ["changelog"])
async def versoes(msg: Message, bot: AsyncTeleBot, args: list[str]) -> None:
    with open(Caminhos.CHANGELOG, "rb") as clog:
        versoes = [Versao(**v) for v in json.loads(clog.read())]
        await bot.send_message(msg.chat.id, TxtSACIM.VERSOES(versoes), parse_mode="HTML")


# Comandos que enviam o banner (logo)


@criar_comando("start", "Sobre o Bot", ["sobre", "about"])
async def start(msg: Message, bot: AsyncTeleBot, args: list[str]) -> None:
    with open(Caminhos.LOGO, "rb") as logo:
        await bot.send_photo(msg.chat.id, logo, caption=TxtSACIM.START, parse_mode="HTML")


@criar_comando("help", "Sobre os Comandos", ["ajuda"])
async def help(msg: Message, bot: AsyncTeleBot, args: list[str]) -> None:
    with open(Caminhos.LOGO, "rb") as logo:
        await bot.send_photo(msg.chat.id, logo)
        await bot.send_message(msg.chat.id, TxtSACIM.HELP, parse_mode="HTML")


# Envio de arquivos


@criar_comando(nome="cal2026", descricao="Calendário Escolar 2026")
async def cal2026(msg: Message, bot: AsyncTeleBot, args: list[str]) -> None:
    with open(Caminhos.A_CAL_2026, "rb") as doc:
        # Responde o bot
        await bot.send_document(
            msg.chat.id,
            doc,
            caption=TxtArquivos.CALENDARIO(2026),
            parse_mode="HTML",
        )


@criar_comando(nome="cal2027", descricao="Calendário Escolar 2027")
async def cal2027(msg: Message, bot: AsyncTeleBot, args: list[str]) -> None:
    with open(Caminhos.A_CAL_2027, "rb") as doc:
        # Responde o bot
        await bot.send_document(
            msg.chat.id,
            doc,
            caption=TxtArquivos.CALENDARIO(2027),
            parse_mode="HTML",
        )


@criar_comando(nome="matriculas", descricao="Informativo de matrículas")
async def matriculas(msg: Message, bot: AsyncTeleBot, args: list[str]) -> None:
    with open(Caminhos.A_MATRICULAS, "rb") as doc:
        # Responde o bot
        await bot.send_document(
            msg.chat.id,
            doc,
            caption=TxtArquivos.MATRICULAS,
            parse_mode="HTML",
        )
