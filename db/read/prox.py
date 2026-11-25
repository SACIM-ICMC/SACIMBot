from typing import Any

from rapidfuzz import fuzz

from db.conexao import conectar


# Retorna todas as colunas de retorno de resultados encontrados
# na busca de 'busca' na coluna 'coluna_de_busca' na tabela 'tabela'
# em que o termo buscado se *aproxima* do termo real na tabela
def buscar_por_proximidade(
    busca: str,
    tabela: str,
    coluna_de_busca: str,
    colunas_de_retorno: list[str],
    limite: int | None = None,
    max_resultados: int | None = None,
) -> tuple[bool, list[dict[str, Any]]]:
    with conectar() as conn:
        # Adiciona a coluna de busca na lista para também selecioná-la na busca
        cols = [coluna_de_busca, *list(colunas_de_retorno)]

        busca = busca.strip().lower()
        busca_split = busca.split()

        # Se a busca é vazia, para
        if not busca_split:
            return False, []

        # FORMATA O COMANDO
        params = [f"%{p}%" for p in busca_split]
        txt_limite = "" if not limite else f"LIMIT {limite}"
        # Realiza a busca primeiro com a condição AND e, se não encontrar nada, com a OR
        comando_and = f"""
            SELECT {", ".join(cols)} FROM {tabela}
            WHERE {" AND ".join([f"{coluna_de_busca} LIKE ?" for _ in busca_split])}
            {txt_limite}    
        """
        comando_or = f"""
            SELECT {", ".join(cols)} FROM {tabela}
            WHERE {" OR ".join([f"{coluna_de_busca} LIKE ?" for _ in busca_split])}
            {txt_limite}    
        """
        res = (
            conn.execute(comando_and, params).fetchall()
            or conn.execute(comando_or, params).fetchall()
        )
        # Se não encontrou nada, para
        if not res:
            return False, []

        res_score = []

        for r in res:
            termo_encontrado = r[0].lower()

            score = fuzz.token_set_ratio(busca, termo_encontrado) / 100.0
            # Bônus para nomes que começam com o primeiro termo buscado
            score += 0.15 if termo_encontrado.startswith(busca_split[0]) else 0.0
            # Bônus de proximidade de tamanho
            score += (len(busca) / len(termo_encontrado)) * 0.1

            # Adiciona o resultado da busca no vetor (remove o 'nome' do começo)
            res_score.append(
                {
                    "score": round(score, 4),
                    "cols": dict(zip(colunas_de_retorno, r[1:], strict=True)),
                }
            )

        # Ordena pelo score decrescente
        res_score.sort(key=lambda x: x["score"], reverse=True)
        # Limita as respostas do array
        if max_resultados:
            res_score = res_score[:max_resultados]

        # Verifica se um dos resultados encontrados é expressivamente mais provável
        auto_sugerir = len(res_score) == 1 or (res_score[0]["score"] - res_score[1]["score"]) > 0.20

        return auto_sugerir, [r["cols"] for r in res_score if r["score"] > 0.40]
