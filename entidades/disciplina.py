import json
from dataclasses import asdict, dataclass

from entidades.pessoa import Pessoa


@dataclass(slots=True)
class Disciplina:
    # Informações gerais
    unidade: str
    departamento: str | None
    codigo: str
    nome: str
    nome_ingles: str | None
    tipo: str
    data_ativacao: str
    data_desativacao: str | None
    # Créditos
    creditos_aula: int
    creditos_trab: int
    carga_horaria: int
    carga_horaria_extensao: int | None
    # Atividades de extensão
    grupos_ext: str | None
    objetivos_ext: str | None
    descricao_ext: str | None
    indicadores_ext: str | None
    # Descrições textuais
    ementa: str
    objetivos: str
    conteudo: str
    metodo_avaliacao: str
    criterios_avaliacao: str
    recuperacao: str
    bibliografia: str
    # Docentes responsáveis
    docentes_responsaveis: list[Pessoa]

    # Converte de dicionário
    @classmethod
    def from_dict(cls, dados: dict) -> "Disciplina":
        dados = dados.copy()  # Copia o objeto

        dados["docentes_responsaveis"] = [Pessoa(**p) for p in dados["docentes_responsaveis"]]
        return cls(**dados)

    # Retorna a linha formatada para inserção no SQL
    def gerar_linha_sql(self) -> tuple:
        return (
            self.unidade,
            self.departamento,
            self.nome,
            self.nome_ingles,
            self.creditos_aula,
            self.creditos_trab,
            self.carga_horaria,
            self.carga_horaria_extensao,
            self.tipo,
            self.data_ativacao,
            self.data_desativacao,
            self.ementa,
            self.objetivos,
            self.conteudo,
            self.metodo_avaliacao,
            self.criterios_avaliacao,
            self.recuperacao,
            self.bibliografia,
            self.grupos_ext,
            self.objetivos_ext,
            self.descricao_ext,
            self.indicadores_ext,
            json.dumps(asdict(self), ensure_ascii=False),
        )
