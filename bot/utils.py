import re

from telebot.formatting import hlink


# Checagem de argumentos
def check_args(args: list[str]) -> bool:
    return args


# Formatações


def formatar_email(email: str) -> str:
    return hlink(email, "mailto:" + email)


def formatar_sala(entrada: str) -> str:
    if not entrada or not isinstance(entrada, str):
        return None

    # Remove espaços extras nas pontas e a palavra "sala"
    texto = re.sub(r"^(?:sala|SALA)\s*", "", entrada.strip(), flags=re.IGNORECASE)

    # Padrão com separador (hífen, ponto, underline ou espaço)
    padrao_com_sep = r"^(\d+)[\s\-_.]+(\d+)[\s\-_.]*([a-zA-Z])?$"
    # Padrão sem separador
    padrao_sem_sep = r"^(\d+)(\d{3})[\s\-_.]*([a-zA-Z])?$"
    if not (match := re.match(padrao_com_sep, texto) or re.match(padrao_sem_sep, texto)):
        return None
    # Retorna os valores encontrados
    bloco, num, complemento = match.groups()
    return f"{bloco}-{num}{'' if not complemento else f' {complemento.upper()}'}"
