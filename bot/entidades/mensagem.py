from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, LinkPreviewOptions, Message

from bot.entidades.botao import gerar_botoes_da_msg_lista, gerar_botoes_do_menu
from bot.entidades.callback import CallbackData as CD
from bot.entidades.menu import Menu
from bot.entidades.resultados import ResDeBusca, Resultado
from bot.textos.disciplinas import TxtDisc
from bot.textos.pesquisas import TxtPesquisa
from bot.textos.pessoas import TxtPessoa
from bot.textos.resultados import TxtResDeBusca
from bot.textos.utils import TXT_DICA_MENU_NAVEGACAO
from entidades.disciplina import Disciplina
from entidades.oferecimento import HorarioOfcProfessor, Oferecimento
from entidades.pesquisa import Pesquisa
from entidades.pessoa import PessoaICMC
from entidades.requisito import Requisito

MSGS_COM_BOTOES_DINAMICOS: dict[str, "MsgComBotoesDinamicos"] = {}


# Classe principal, que gerencia uma mensagem com botões
@dataclass
class MsgComBotoesDinamicos(ABC):
    bot: AsyncTeleBot
    id_usuario: int

    data_criacao: datetime = field(init=False)
    id_custom: str = field(init=False)
    msg: Message = field(init=False)
    txt: str = field(init=False)
    botoes: InlineKeyboardMarkup | None = field(init=False)

    def __post_init__(self) -> None:
        # Definição da data (para limpeza automática)
        self.data_criacao = datetime.now()
        # Inserção no dicionário
        self.id_custom = uuid4().hex
        MSGS_COM_BOTOES_DINAMICOS[self.id_custom] = self

    async def enviar_primeira_mensagem(self, identificador: Message | int) -> None:
        # Envia e atribui a mensagem à classe
        self.atualizar_msg()
        if isinstance(identificador, int):
            self.msg = await self.bot.send_message(
                chat_id=identificador,
                text=self.txt,
                reply_markup=self.botoes,
                link_preview_options=LinkPreviewOptions(True),
                parse_mode="HTML",
            )
        elif isinstance(identificador, Message):
            self.msg = await self.bot.reply_to(
                message=identificador,
                text=self.txt,
                reply_markup=self.botoes,
                link_preview_options=LinkPreviewOptions(True),
                parse_mode="HTML",
            )
        else:
            raise ValueError("O identificador precisa ser um id ou uma mensagem!")

    async def editar_mensagem(self) -> None:
        # Edita a mensagem
        await self.bot.edit_message_text(
            text=self.txt,
            chat_id=self.msg.chat.id,
            message_id=self.msg.id,
            reply_markup=self.botoes,
            link_preview_options=LinkPreviewOptions(True),
            parse_mode="HTML",
        )

    def remover_do_dict(self) -> None:
        # Retira do dicionário
        MSGS_COM_BOTOES_DINAMICOS.pop(self.id_custom, None)

    def atualizar_msg(self) -> None:
        self.set_texto()
        self.set_botoes()

    @abstractmethod
    def set_texto(self) -> None:
        pass

    @abstractmethod
    def set_botoes(self) -> None:
        pass

    # Trata o callback
    @abstractmethod
    async def executar_acao(self, *args: str) -> None:
        pass

    # Finaliza a mensagem
    @abstractmethod
    async def finalizar(self) -> None:
        pass


@dataclass
class MsgMenu(MsgComBotoesDinamicos, ABC):
    menu: Menu = field(init=False)
    tipo_menu: CD.TipoMenu = field(init=False)
    lista_menus: tuple[CD.ItemMenu] = field(init=False)

    def __post_init__(self) -> None:
        # Garantia de condições
        if len(self.lista_menus) == 0:
            raise ValueError("A lista de menus não pode estar vazia!")

        super().__post_init__()  # Criação do ID
        self.menu = Menu(self.tipo_menu, self.lista_menus)

    def set_botoes(self) -> None:
        self.botoes = gerar_botoes_do_menu(self.menu, self.id_custom)

    # Recebe o código para mudar o menu
    async def executar_acao(self, *args: str) -> None:
        # Telegram não deixa editar mensagem se manter o mesmo texto e botões
        if self.menu.mudar_menu(args[0]):
            self.atualizar_msg()
            await self.editar_mensagem()

    async def finalizar(self) -> None:
        self.remover_do_dict()  # Retira do dicionário


@dataclass
class MsgDisciplina(MsgMenu):
    disciplina: Disciplina
    requisitos: list[Requisito]
    oferecimentos: list[Oferecimento]
    # Estáticos
    tipo_menu = CD.TipoMenu.DISCIPLINA
    lista_menus = (
        CD.ItemMenu.CAPA_DISC,
        CD.ItemMenu.EMENTA,
        CD.ItemMenu.AVALIACAO,
        CD.ItemMenu.BIBLIOGRAFIA,
        CD.ItemMenu.REQUISITOS,
        CD.ItemMenu.OFERECIMENTOS,
    )

    def set_texto(self) -> None:
        cod = self.disciplina.codigo
        nome = self.disciplina.nome

        match self.menu.menu_atual:
            case CD.ItemMenu.CAPA_DISC:
                self.txt = TxtDisc.DISC(self.disciplina)
            case CD.ItemMenu.EMENTA:
                self.txt = TxtDisc.EMENTA(self.disciplina)
            case CD.ItemMenu.AVALIACAO:
                self.txt = TxtDisc.AVALIACAO(self.disciplina)
            case CD.ItemMenu.BIBLIOGRAFIA:
                self.txt = TxtDisc.BIBLIOGRAFIA(self.disciplina)
            case CD.ItemMenu.REQUISITOS:
                self.txt = TxtDisc.REQUISITOS(cod, nome, self.requisitos)
            case CD.ItemMenu.OFERECIMENTOS:
                self.txt = TxtDisc.OFERECIMENTOS(cod, nome, self.oferecimentos)
        self.txt += TXT_DICA_MENU_NAVEGACAO


@dataclass
class MsgPessoa(MsgMenu):
    pessoa: PessoaICMC
    pesquisas: list[str]
    horarios: list[HorarioOfcProfessor]
    # Estáticos
    tipo_menu = CD.TipoMenu.PESSOA
    lista_menus = (CD.ItemMenu.CAPA_PESSOA, CD.ItemMenu.HORARIOS)

    def set_texto(self) -> None:
        match self.menu.menu_atual:
            case CD.ItemMenu.CAPA_PESSOA:
                self.txt = TxtPessoa.PESSOA(self.pessoa, self.pesquisas)
            case CD.ItemMenu.HORARIOS:
                self.txt = TxtPessoa.HORARIOS(self.pessoa.nome, self.horarios)
        self.txt += TXT_DICA_MENU_NAVEGACAO


@dataclass
class MsgPesquisa(MsgMenu):
    pesquisa: Pesquisa
    # Estáticos
    tipo_menu = CD.TipoMenu.PESQUISA

    def __post_init__(self) -> None:
        # Monta a lista de menus
        lista = [CD.ItemMenu.CAPA_PESQ]
        if self.pesquisa.linhas:
            lista.append(CD.ItemMenu.LINHAS)
        self.lista_menus = tuple(lista)

        super().__post_init__()

    def set_texto(self) -> None:
        match self.menu.menu_atual:
            case CD.ItemMenu.CAPA_PESQ:
                self.txt = TxtPesquisa.PESQUISA(self.pesquisa)
            case CD.ItemMenu.LINHAS:
                self.txt = TxtPesquisa.LINHAS(self.pesquisa.nome, self.pesquisa.linhas)
        self.txt += TXT_DICA_MENU_NAVEGACAO


@dataclass
class MsgListaDeResultados(MsgComBotoesDinamicos):
    lista: list[Resultado]
    termo_buscado: str
    tipo_res: CD.ItemPg
    item_por_pg: int = 5

    res: ResDeBusca = field(init=False)
    nome_entidade: str = field(init=False)

    def __post_init__(self) -> None:
        super().__post_init__()  # Criação do ID
        # Inicializações
        self.res = ResDeBusca(self.lista, self.tipo_res, self.item_por_pg)
        nomes = {
            CD.ItemPg.PESSOA: "pessoas",
            CD.ItemPg.PESQUISA: "pesquisas",
            CD.ItemPg.DISCIPLINA: "disciplinas",
            CD.ItemPg.COMISSAO: "comissões",
        }
        self.nome_entidade = nomes[self.tipo_res]

    def set_texto(self) -> None:
        self.txt = TxtResDeBusca.LISTA(self.res, self.termo_buscado, self.nome_entidade)

    def set_botoes(self) -> None:
        self.botoes = gerar_botoes_da_msg_lista(self.res, self.id_custom, self.tipo_res)

    # Recebe o código para mover a página
    async def executar_acao(self, *args: str) -> None:
        # Telegram não deixa editar mensagem se manter o mesmo texto e botões
        if self.res.mover_pagina(args[0]):
            self.atualizar_msg()
            await self.editar_mensagem()

    async def finalizar(self) -> None:
        self.remover_do_dict()  # Retira do dicionário
        await self.bot.delete_message(self.msg.chat.id, self.msg.id)  # Remove a mensagem
