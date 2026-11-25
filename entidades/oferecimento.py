import json
from dataclasses import asdict, dataclass


@dataclass(slots=True)
class DocenteTabelaHorario:
    nome: str | None
    tipo: str | None


@dataclass(slots=True)
class Horario:
    dia: str | None
    horario_inicio: str | None
    horario_termino: str | None
    professores: list[DocenteTabelaHorario]

    # Converte de dicionário
    @classmethod
    def from_dict(cls, dados: dict) -> "Horario":
        dados = dados.copy()  # Copia o objeto

        dados["professores"] = [DocenteTabelaHorario(**dth) for dth in dados["professores"]]
        return cls(**dados)

    # Retorna a linha formatada para inserção no SQL
    def gerar_linha_sql(self) -> tuple:
        return (
            self.dia,
            self.horario_inicio,
            self.horario_termino,
            json.dumps(asdict(self), ensure_ascii=False),
        )


@dataclass(slots=True)
class DocenteTabelaAtiv:
    nome: str | None
    tipo: str | None
    tipo_atividade: str | None
    carga_horaria: int | None

    # Retorna a linha formatada para inserção no SQL
    def gerar_linha_sql(self) -> tuple:
        return (self.nome, self.tipo, self.tipo_atividade, self.carga_horaria)


@dataclass(slots=True)
class Oferecimento:
    codigo_turma: str | None
    obs_turma: str | None
    inicio: str | None
    fim: str | None
    tipo: str | None
    obs: str | None
    horarios: list[Horario]
    atividades: list[DocenteTabelaAtiv]

    # Converte de dicionário
    @classmethod
    def from_dict(cls, dados: dict) -> "OferecimentosDisciplina":
        dados = dados.copy()  # Copia o objeto

        dados["horarios"] = [Horario.from_dict(h) for h in dados["horarios"]]
        dados["atividades"] = [DocenteTabelaAtiv(**dta) for dta in dados["atividades"]]
        return cls(**dados)

    # Retorna a linha formatada para inserção no SQL
    def gerar_linha_sql(self) -> tuple:
        return (
            self.codigo_turma,
            self.obs_turma,
            self.inicio,
            self.fim,
            self.tipo,
            self.obs,
            json.dumps(asdict(self), ensure_ascii=False),
        )


@dataclass(slots=True)
class OferecimentosDisciplina:
    codigo: str
    oferecimentos: list[Oferecimento]

    # Converte de dicionário
    @classmethod
    def from_dict(cls, dados: dict) -> "OferecimentosDisciplina":
        dados = dados.copy()  # Copia o objeto

        dados["oferecimentos"] = [Oferecimento.from_dict(of) for of in dados["oferecimentos"]]
        return cls(**dados)


@dataclass(slots=True)
class HorarioOfcProfessor:
    nome: str
    cod_disc: str
    cod_turma: str
    obs: str
    horario: Horario

    # Converte de tuplas
    @classmethod
    def from_tupla(cls, tupla: tuple) -> "HorarioOfcProfessor":
        if len(tupla) != 5:
            raise ValueError("Quantidade inesperada de elementos na tupla!")

        lista = list(tupla)
        lista[4] = Horario.from_dict(json.loads(lista[4]))  # Converte os horários
        return cls(lista[0], lista[1], lista[2], lista[3], lista[4])
