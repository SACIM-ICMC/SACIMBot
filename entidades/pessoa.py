import json
from dataclasses import asdict, dataclass, field

from constantes import NomesDeptos


@dataclass(slots=True)
class Pessoa:
    nome: str | None
    nusp: str | None


@dataclass(slots=True)
class PessoaICMC(Pessoa):
    email: str | None  # Apenas obtido para pessoas do ICMC
    id_site: str | None  # Apenas coletado para pessoas do ICMC
    profissao: str
    categorias: list[str]
    researcher_id: str | None
    sala: str | None
    pagina: str | None
    telefone: str | None
    lattes: str | None
    grupos_cnpq: str | None

    titulacao: str | None = field(default=None, init=False)
    departamento: str | None = field(default=None, init=False)

    # Definição dos campos de titulação e departamento
    def __post_init__(self) -> None:
        if self.profissao != "Docente":
            return

        match self.categorias[-1]:
            case "MS-6":
                self.titulacao = "Titular"
            case "MS-5":
                self.titulacao = "Associado"
            case "MS-3":
                self.titulacao = "Doutor"

        try:
            self.departamento = NomesDeptos(self.categorias[0].split("-")[1].strip()).name
        except ValueError:
            self.departamento = None

    # Converte de dicionário
    @classmethod
    def from_dict(cls, dados: dict) -> "PessoaICMC":
        dados = dados.copy()  # Copia o objeto
        del dados["titulacao"]
        del dados["departamento"]

        return cls(**dados)

    # Retorna a linha formatada para inserção no SQL
    def gerar_linha_sql(self) -> tuple:
        return (
            self.id_site,
            self.nome,
            self.nusp,
            self.profissao,
            self.titulacao,
            self.departamento,
            json.dumps(self.categorias, ensure_ascii=False),
            self.researcher_id,
            self.email,
            self.sala,
            self.pagina,
            self.telefone,
            self.lattes,
            self.grupos_cnpq,
            json.dumps(asdict(self), ensure_ascii=False),
        )
