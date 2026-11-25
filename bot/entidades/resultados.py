from dataclasses import dataclass, field
from math import ceil

from bot.entidades.callback import CallbackData as CD


@dataclass
class Resultado:
    nome: str
    id_item: str
    # O nome a aparecer na lista
    nome_item: str = None

    def __post_init__(self) -> None:
        if not self.nome_item:
            self.nome_item = self.nome


@dataclass
class ResDeBusca:
    lista: list[Resultado]
    tipo_res: CD.ItemPg
    item_por_pg: int

    # Calculados
    pg_atual: int = field(default=0, init=False)
    nro_pgs: int = field(init=False)
    tam_lista: int = field(init=False)
    inicio: int = field(default=0, init=False)
    fim: int = field(init=False)

    def set_inicio_fim(self) -> None:
        self.inicio = self.pg_atual * self.item_por_pg
        self.fim = min(self.inicio + self.item_por_pg, self.tam_lista)

    def __post_init__(self) -> None:
        # Garante as condições
        if not self.lista:
            raise ValueError("A lista não pode ser vazia!")
        if self.item_por_pg <= 0:
            raise ValueError("item_por_pg tem que ser maior que 0!")

        # Definições
        self.nro_pgs = ceil(len(self.lista) / self.item_por_pg)
        self.tam_lista = len(self.lista)
        self.set_inicio_fim()

    # Mover uma página
    def mover_pagina(self, acao: CD.AcaoPg) -> bool:
        pgs = {
            CD.AcaoPg.PROXIMA: self.pg_atual + 1,
            CD.AcaoPg.ANTERIOR: self.pg_atual - 1,
            CD.AcaoPg.PRIMEIRA: 0,
            CD.AcaoPg.ULTIMA: self.nro_pgs - 1,
        }
        # Verifica a viabilidade de mudar
        nova_pg = max(0, min(pgs[acao], self.nro_pgs - 1))
        if nova_pg == self.pg_atual:
            return False

        self.pg_atual = nova_pg
        self.set_inicio_fim()
        return True
