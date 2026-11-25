import json
from dataclasses import asdict, dataclass


@dataclass(slots=True)
class Curso:
    codigo_curso: str
    codigo_habilitacao: str
    codigo_unidade: str
    nome: str
    unidade: str
    periodo: str
    ativado: int  # 1 para ativado
    link: str

    # Retorna a linha formatada para inserção no SQL
    def gerar_linha_sql(self) -> tuple:
        return (
            self.codigo_curso,
            self.codigo_habilitacao,
            self.codigo_unidade,
            self.nome,
            self.unidade,
            self.periodo,
            self.ativado,
            self.link,
            json.dumps(asdict(self), ensure_ascii=False),
        )
