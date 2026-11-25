import sqlite3

URL_CONEXAO_RO = "file:dados/dados.db?mode=ro"  # Apenas leitura
URL_CONEXAO_RW = "file:dados/dados.db?mode=rw"  # Leitura e escrita

URL_ESQUEMAS = "db/esquemas.txt"


# Conecta no banco de dados e retorna a conexão
def conectar(ro: bool = True) -> sqlite3.Connection:
    # Se for uma conexão de leitura
    if ro:
        return sqlite3.connect(URL_CONEXAO_RO, uri=True)

    # Então é uma conexão de escrita, precisa atualizar o db antes

    # Abre os esquemas
    with open(URL_ESQUEMAS) as f:
        esquemas = f.read()
        # Conecta e executa
        with sqlite3.connect(URL_CONEXAO_RW, uri=True) as conn:
            # Aplica os esquemas
            conn.executescript(esquemas)
            print("Esquemas aplicados.")

    # Agora sim, conecta
    return sqlite3.connect(URL_CONEXAO_RW, uri=True)
