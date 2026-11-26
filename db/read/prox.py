from typing import Any

from rapidfuzz import fuzz
import unicodedata
import re


from db.conexao import conectar

CONECTIVOS = {
    "a",
    "o",
    "as",
    "os",
    "e",
    "de",
    "da",
    "do",
    "das",
    "dos",
    "em",
    "na",
    "no",
    "nas",
    "nos",
    "para",
    "por",
    "com",
    "um",
    "uma",
}
NOTA_MINIMA = 0.45


# Deixa minúsculo, sem acento e sem pontuação
def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", texto.lower()).strip()


# Particiona a string e remove os conectivos apenas se houver algum que não é
def tokenizar(texto: str) -> list[str]:
    todos = normalizar(texto).split()
    uteis = [c for c in todos if c not in CONECTIVOS]
    return uteis or todos


# Compara um token da busca com um token do resultado e pontua
def comparar_tokens(tk_busca: str, tk_res: str) -> float:
    if tk_busca == tk_res:
        return 1.0  # Se for exato
    if len(tk_busca) >= 3 and tk_res.startswith(tk_busca):
        return 0.95  # Se a busca for parte do resultado
    similaridade = fuzz.ratio(tk_busca, tk_res) / 100.0
    return similaridade if similaridade >= 0.8 else 0.0


def pontuar(
    busca_normalizada: str,
    tks_busca: list[str],
    res_normalizado: str,
    tks_res: list[str],
) -> float:
    if busca_normalizada == res_normalizado:
        return 1.0  # Se for exato
    if not tks_res:
        return 0.0  # Se o resultado não tem tokens

    # Quanto da busca foi encontrado no resultado:
    # Para cada token da busca, obtém o maior score que ele atingiu
    # dentre todos os tokens do resultado. Depois, soma todos os scores e normaliza.
    cobertura = sum(
        max(comparar_tokens(tk_busca, tk_res) for tk_res in tks_res) for tk_busca in tks_busca
    ) / len(tks_busca)
    if cobertura == 0:
        return 0.0
    # Quanto do resultado foi encontrado na busca:
    # Para cada token do resultado, obtém o maior score que ele atingiu
    # dentre todos os tokens da busca. Depois, soma todos os scores e normaliza.
    precisao = sum(
        max(comparar_tokens(tk_busca, tk_res) for tk_busca in tks_busca) for tk_res in tks_res
    ) / len(tks_res)

    score = 0.7 * cobertura + 0.3 * precisao
    if res_normalizado.startswith(busca_normalizada):
        score += 0.05
    return min(score, 0.99)  # Só o match exato chega a 1.0


# Retorna todas as colunas de retorno de resultados encontrados
# na busca de 'busca' na coluna 'coluna_de_busca' na tabela 'tabela'
# em que o termo buscado se *aproxima* do termo real na tabela
def buscar_por_proximidade(
    busca: str,
    tabela: str,
    coluna_de_busca: str,
    colunas_de_retorno: list[str],
    max_resultados: int | None = None,
) -> tuple[bool, list[dict[str, Any]]]:
    with conectar() as conn:
        busca_normalizada = normalizar(busca)
        tks_busca = tokenizar(busca)
        if not tks_busca:
            return False, []

        # Adiciona a coluna de busca na lista para também selecioná-la na busca
        cols = [coluna_de_busca, *colunas_de_retorno]
        with conectar() as conn:
            res = conn.execute(f"SELECT {', '.join(cols)} FROM {tabela}").fetchall()

        # Para cada resultado, calcula seu score e filtra se não atingiu a nota mínima
        res_score = []
        for r in res:
            r_normalizado = normalizar(str(r[0]))
            tks_r = tokenizar(str(r[0]))
            score = pontuar(busca_normalizada, tks_busca, r_normalizado, tks_r)
            if score >= NOTA_MINIMA:
                res_score.append(
                    {
                        "score": round(score, 4),
                        "termo": r_normalizado,
                        "cols": dict(zip(colunas_de_retorno, r[1:], strict=True)),
                    }
                )
        # Se nenhum atingiu a nota mínima, para
        if not res_score:
            return False, []

        # Ordena pelo score (decrescente)
        res_score.sort(key=lambda x: (-x["score"],))
        # Limita o número de resultados
        if max_resultados:
            res_score = res_score[:max_resultados]

        # Verifica se um dos resultados encontrados é expressivamente mais provável
        auto_sugerir = len(res_score) == 1 or (res_score[0]["score"] - res_score[1]["score"]) > 0.15
        # Se for, retorna só ele
        if auto_sugerir:
            return True, [res_score[0]["cols"]]
        # Se não, ordena por ordem alfabética
        res_score.sort(key=lambda x: (x["termo"],))
        return False, [r["cols"] for r in res_score]
