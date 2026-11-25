from dataclasses import dataclass


@dataclass(slots=True)
class Versao:
    versao: str
    data: str
    novidades: list[str]
    correcoes: list[str]
