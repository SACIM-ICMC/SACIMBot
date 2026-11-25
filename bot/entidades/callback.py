from enum import StrEnum


# Montagem das strings de callback
class CallbackData:
    # IDs dos callbacks
    class AcaoPg(StrEnum):
        PRIMEIRA = "sbw"
        ANTERIOR = "bwd"
        PROXIMA = "fwd"
        ULTIMA = "sfw"

    class ItemPg(StrEnum):
        PESSOA = "pid"
        DISCIPLINA = "did"
        PESQUISA = "qid"
        COMISSAO = "cid"

    class TipoMenu(StrEnum):
        PESSOA = "pss"
        DISCIPLINA = "dsc"
        PESQUISA = "psq"

    class ItemMenu(StrEnum):
        # Pessoas
        CAPA_PESSOA = "pss"
        HORARIOS = "hor"
        # Disciplinas
        CAPA_DISC = "dsc"
        EMENTA = "emt"
        AVALIACAO = "avl"
        BIBLIOGRAFIA = "bbg"
        EXTENSAO = "ext"
        REQUISITOS = "req"
        OFERECIMENTOS = "ofc"
        # Pesquisa
        CAPA_PESQ = "psq"
        LINHAS = "lnh"

    # Se uma string pertence a um tipo
    @staticmethod
    def pertence(tipo: StrEnum, valor: str) -> bool:
        return valor in tipo._value2member_map_

    # Geradores de callbacks
    @staticmethod
    def pg_ctrl(id_pg: str, tipo: AcaoPg) -> str:
        return f"pg:{id_pg}:{tipo.value}:"

    @staticmethod
    def pg_item(id_pg: str, tipo: ItemPg, id_entidade: str) -> str:
        return f"pg:{id_pg}:{tipo.value}:{id_entidade}"

    @staticmethod
    def menu_item(id_menu: str, item_menu: ItemMenu) -> str:
        return f"menu:{id_menu}:{item_menu.value}:"

    @staticmethod
    def nop() -> str:
        return "nop"

    # PARSERS
    @staticmethod
    def parse(data: str) -> tuple[str]:
        return data.split(":")[1:]
