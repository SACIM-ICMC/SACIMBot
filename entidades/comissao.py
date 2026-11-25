import json
from dataclasses import asdict, dataclass


@dataclass(slots=True)
class MembroComissao:
    nome: str
    nusp: str
    categ_colegiado: str  # Ex.: Departamento de Ciências de Computação - SCC
    func_colegiado: str  # Ex.: Titular
    func_membro: str  # Ex.: Chefe de Departamento
    inicio_mandato: str
    fim_mandato: str

    # Retorna a linha formatada para inserção no SQL
    def gerar_linha_sql(self) -> tuple:
        return (
            self.nome,
            self.nusp,
            self.categ_colegiado,
            self.func_colegiado,
            self.func_membro,
            self.inicio_mandato,
            self.fim_mandato,
            json.dumps(asdict(self), ensure_ascii=False),
        )


@dataclass(slots=True)
class Comissao:
    nome: str
    link: str
    codigo: str
    sigla: str
    membros: list[MembroComissao]

    # Converte de dicionário
    @classmethod
    def from_dict(cls, dados: dict) -> "Comissao":
        dados = dados.copy()  # Copia o objeto

        dados["membros"] = [MembroComissao(**m) for m in dados["membros"]]
        return cls(**dados)

    # Obtém a presidência da comissão
    def obter_presidencia(self) -> "Chapa":
        pres = next((m for m in self.membros if m.func_colegiado == "Presidente"), None)
        vice = next((m for m in self.membros if m.func_colegiado == "Vice-Presidente"), None)
        return Chapa(
            PessoaChapa(pres.nome, pres.nusp) if pres is not None else None,
            PessoaChapa(vice.nome, vice.nusp) if vice is not None else None,
        )

    # Retorna a linha formatada para inserção no SQL
    def gerar_linha_sql(self) -> tuple:
        return (
            self.codigo,
            self.sigla,
            self.nome,
            self.link,
            json.dumps(asdict(self), ensure_ascii=False),
        )


@dataclass(slots=True)
class PessoaChapa:
    nome: str | None
    nusp: str | None
    email: str | None = None


@dataclass(slots=True)
class Chapa:
    pres: PessoaChapa | None = None
    vice: PessoaChapa | None = None
