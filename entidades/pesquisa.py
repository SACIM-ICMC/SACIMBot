import json
from dataclasses import asdict, dataclass


@dataclass(slots=True)
class Lab:
    nome: str
    link: str


@dataclass(slots=True)
class Docente:
    nome: str
    id_site: str


@dataclass(slots=True)
class Pesquisa:
    nome: str
    id_site: str
    area: str
    linhas: list[str]
    labs: list[Lab]
    docentes: list[Docente]

    # Converte de dicionário
    @classmethod
    def from_dict(cls, dados: dict) -> "Pesquisa":
        dados = dados.copy()  # Copia o objeto

        dados["labs"] = [Lab(**d) for d in dados["labs"]]
        dados["docentes"] = [Docente(**d) for d in dados["docentes"]]
        return cls(**dados)

    # Retorna a linha formatada para inserção no SQL
    def gerar_linha_sql(self) -> tuple:
        return (
            self.id_site,
            self.nome,
            self.area,
            json.dumps(asdict(self), ensure_ascii=False),
        )
