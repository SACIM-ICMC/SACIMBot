import json
from dataclasses import asdict, dataclass


@dataclass(slots=True)
class Requisito:
    codigo_curso: str
    nome_curso: str
    periodo_ideal: str
    id_grupo: str
    codigo_requisito: str
    nome_requisito: str
    tipo: str

    # Retorna a linha formatada para inserção no SQL
    def gerar_linha_sql(self) -> tuple:
        return (
            self.codigo_curso,
            self.nome_curso,
            self.periodo_ideal,
            self.codigo_requisito,
            self.nome_requisito,
            self.tipo,
            self.id_grupo,
            json.dumps(asdict(self), ensure_ascii=False),
        )


@dataclass(slots=True)
class RequisitosDisciplina:
    codigo: str
    requisitos: list[Requisito]

    # Converte de dicionário
    @classmethod
    def from_dict(cls, dados: dict) -> "RequisitosDisciplina":
        dados = dados.copy()  # Copia o objeto

        dados["requisitos"] = [Requisito(**r) for r in dados["requisitos"]]
        return cls(**dados)
