from telebot.formatting import hbold


class TxtOfc:
    def SIGLA_INVALIDA() -> str:
        return "❌ Verifique a sigla do departamento e tente novamente."

    def OFERECIMENTO(depto: str, links: list[str]) -> str:
        txt = (
            f"Disciplinas do departamento {hbold(depto)} "
            f"no {hbold('primeiro semestre')}: {links[0]}\n\n"
        )
        if len(links) == 1:
            return txt + "❌ Ainda não foram encontradas disciplinas do segundo semestre."

        return txt + (
            f"Disciplinas do departamento {hbold(depto)} no {hbold('segundo semestre')}: {links[1]}"
        )
