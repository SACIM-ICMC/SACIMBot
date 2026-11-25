from enum import IntEnum, StrEnum

MAX_RESULTADOS = 5


DIAS = {
    "seg": "Segunda-feira",
    "ter": "Terça-feira",
    "qua": "Quarta-feira",
    "qui": "Quinta-feira",
    "sex": "Sexta-feira",
    "sab": "Sábado",
    "dom": "Domingo",
}


# Códigos das CoCs
class CodigosCoCs(IntEnum):
    BCC = 15
    BSI = 14
    BCDados = 100  # Por que o BCDados é 100?
    BECD = 12
    BMA = 10
    LMA = 11
    BMACC = 13


# Códigos e nomes dos Deptos
class CodigosDeptos(IntEnum):
    SCC = 1947
    SSC = 3385
    SMA = 1949
    SME = 3298


class NomesDeptos(StrEnum):
    SCC = "Ciências de Computação"
    SSC = "Sistemas de Computação"
    SMA = "Matemática"
    SME = "Matemática Aplicada e Estatística"


class SiglasComissoes(StrEnum):
    COC = "CoC"
    DEPTO = "CoDepto"


class RedesSACIM(StrEnum):
    INSTAGRAM = "@sacim.caaso"
    URL_INSTAGRAM = "https://www.instagram.com/sacim.caaso/"
    EMAIL_GMAIL = "sacim.caaso@gmail.com"
    EMAIL_ICMC = "sacim@icmc.usp.br"
    LINKTREE = "linktr.ee/sacim"
    URL_LINKTREE = "https://linktr.ee/sacim"
    SITE = "sacim.icmc.usp.br"
    URL_SITE = "http://sacim.icmc.usp.br"
    REPO = "https://github.com/SACIM-ICMC/SACIMBot"


class LinksInvite(StrEnum):
    SACIM_AVISOS = "https://t.me/SACIM"
    SUPERFAMILIA = "https://t.me/joinchat/bakayQMJ5rkwYTZh"
    AVALIACOES = "https://t.me/+pXJDzgfnakQwNzNh"
    ASSALTOS = "https://t.me/joinchat/Ckw0K04Dn4qnqNabFFhSnQ"
    SUPERFEIRAO = "https://t.me/+9sNawgOy8NpjMjEx"
    PROMOCOES = "https://t.me/+HH8l_gHktcg0MWEx"
    RESTAURANTES = "https://t.me/+3wwcCJM35udkMWIx"
    ROLES = "https://t.me/+8W-wVzVQ_KQyNjA5"


class EmailsGrad(StrEnum):
    BCC = "secbcc@icmc.usp.br"
    BSI = "secbsi@icmc.usp.br"
    BECD = "secbecd@icmc.usp.br"
    BCDADOS = "secbcdados@icmc.usp.br"
    BMA_LMA = "secmat@icmc.usp.br"
    BMACC = "secbmacc@icmc.usp.br"
    EC_LCE = "grad@icmc.usp.br"
    ESTAGIO = "estagiograd@icmc.usp.br"
    COMUN_EXT = "grad@icmc.usp.br"


class EmailsICMC(StrEnum):
    EVENTOS = "eventos@icmc.usp.br"


class Biblio(StrEnum):
    EMAIL = "biblio@icmc.usp.br"
    WHATS = "+55 16 3373-9637"
    LIVECHAT = "http://biblioteca.icmc.usp.br/livechat/"


class Museu(StrEnum):
    SITE = "https://mc.icmc.usp.br"
    EMAIL = "museu@icmc.usp.br"
    WHATS = "(16) 3373-9754"


class LinksInfos(StrEnum):
    INTRANET_SALAS = "https://intranet.icmc.usp.br/salas/salas.php"
    RESERVAS = "https://docs.google.com/forms/d/e/1FAIpQLScd4_-aVu6FgFiGq9lojbWDDGortRZcaR1SdxV5BwUeQUeE-w/viewform?pli=1&pli=1"
    PRINTER = "https://printer.icmc.usp.br"
    GUIA_EDUROAM = (
        "https://atendimentosti.usp.br/otrs/public.pl?Action=PublicFAQExplorer;CategoryID=37"
    )
    GUIA_VPN = "https://atendimentosti.usp.br/otrs/public.pl?Action=PublicFAQExplorer;CategoryID=12"
    CARTILHAS_SACIM = "https://tr.ee/Ytwmmx666B"


class Caminhos(StrEnum):
    PASTA_COMANDOS = "bot/comandos"
    CURSOS = "dados/json/cursos.json"
    PESQUISAS = "dados/json/pesquisas.json"
    LISTA_PESSOAS = "dados/json/lista_pessoas.json"
    PESSOAS = "dados/json/pessoas.json"
    COMISSOES = "dados/json/comissoes.json"
    PASTA_DISCS = "dados/json/discs/"
    PASTA_OFCS = "dados/json/ofcs/"
    PASTA_REQS = "dados/json/reqs/"
    A_CAL_2026 = "arquivos/docs/calendario2026.pdf"
    A_CAL_2027 = "arquivos/docs/calendario2027.pdf"
    A_MATRICULAS = "arquivos/docs/matriculas.pdf"
    LOGO = "arquivos/logo.png"
    COMANDOS_UTEIS = "bot/comandos_uteis.txt"
    CHANGELOG = "changelog.json"

    @staticmethod
    def CMD(cmd: str) -> str:
        return f"bot.comandos.{cmd}"

    @staticmethod
    def DISC(cod_uni: str) -> str:
        return f"dados/json/discs/{cod_uni}.json"

    @staticmethod
    def OFC(cod_uni: str) -> str:
        return f"dados/json/ofcs/{cod_uni}.json"

    @staticmethod
    def REQ(cod_uni: str) -> str:
        return f"dados/json/reqs/{cod_uni}.json"


class URLJupiter(StrEnum):
    UNIDADES = "https://uspdigital.usp.br/jupiterweb/jupColegiadoLista?tipo=D"

    @staticmethod
    def DISCIPLINAS_DA_UNIDADE(cod_uni: str) -> str:
        return f"https://uspdigital.usp.br/jupiterweb/jupDisciplinaLista?codcg={cod_uni}&letra=A-Z&tipo=D"

    # tipo: "N" para ativos, "V" para inativos
    @staticmethod
    def CURSOS_DA_UNIDADE(cod_uni: str, tipo: str) -> str:
        return f"https://uspdigital.usp.br/jupiterweb/jupCursoLista?codcg={cod_uni}&tipo={tipo}"

    @staticmethod
    def DISCIPLINA(cod_disc: str) -> str:
        return f"https://uspdigital.usp.br/jupiterweb/obterDisciplina?nomdis=&sgldis={cod_disc}"

    @staticmethod
    def REQUISITOS(cod_disc: str) -> str:
        return f"https://uspdigital.usp.br/jupiterweb/listarCursosRequisitos?coddis={cod_disc}"

    @staticmethod
    def OFERECIMENTOS(cod_disc: str) -> str:
        return f"https://uspdigital.usp.br/jupiterweb/obterTurma?sgldis={cod_disc}"

    # tipo: "N" para ativos, "V" para inativos
    @staticmethod
    def CURSO(cod_uni: str, cod_curso: str, cod_hab: str, tipo: str) -> str:
        return f"https://uspdigital.usp.br/jupiterweb/listarGradeCurricular?codcg={cod_uni}&codcur={cod_curso}&codhab={cod_hab}&tipo={tipo}"


class URLICMC(StrEnum):
    ROOT = "https://icmc.usp.br"
    PESSOAS = "https://icmc.usp.br/pessoas"
    GRUPOS_PESQUISA = "https://www.icmc.usp.br/pesquisa/grupos"
    COMISSOES = "https://icmc.usp.br/institucional/estrutura-administrativa"
    OFERECIMENTOS_ICMC = "https://icmc.usp.br/graduacao/informacoes-gerais-e-servicos/horarios-de-aulas"

    @staticmethod
    def PESSOA(p_id: str) -> str:
        return f"https://icmc.usp.br/pessoas?id={p_id}"

    @staticmethod
    def RESEARCHER_ID(r_id: str) -> str:
        return f"http://www.researcherid.com/rid/{r_id}"

    @staticmethod
    def PESQUISA(p_id: str) -> str:
        return f"https://icmc.usp.br/pesquisa/grupos/?lab={p_id}"


URL_PROXY_PORTAL_SERVICOS = (
    "https://portalservicos.usp.br/proxy/uspproc/listar/marteweb/pubListarParticipanteColeg"
)


def URL_PESSOA_BUSCAR(pesquisa: str) -> str:
    return f"https://uspdigital.usp.br/mundus/pessoaBuscar?codpes=&nompes={pesquisa}&submit=Buscar&print=s&buscar=s&tipo=&f=form1&c1=c1&c2=c2"
