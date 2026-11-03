
import random
import pandas as pd


def verificar_oito_rainhas(solucao: str) -> bool:
    """Verifica se uma string de 8 caracteres resolve o problema das 8 rainhas."""
    if len(solucao) != 8 or not solucao.isdigit():
        return False

    linhas = [int(c) - 1 for c in solucao]

    for col1 in range(8):
        for col2 in range(col1 + 1, 8):
            lin1 = linhas[col1]
            lin2 = linhas[col2]

            # Mesma linha
            if lin1 == lin2:
                return False

            # Mesma diagonal
            if abs(lin1 - lin2) == abs(col1 - col2):
                return False

    return True


def criar_dataset_alternado(tamanho: int) -> pd.DataFrame:
    """Gera um DataFrame alternando entre sequências puramente aleatórias

    e sequências aleatórias sem repetição de caracteres.
    """
    dados = []
    digitos_base = ["1", "2", "3", "4", "5", "6", "7", "8"]

    for i in range(tamanho):
        if i % 3 == 0:
            # Modo Atual: Completamente Aleatório
            possivel_solucao = "".join(
                str(random.randint(1, 8)) for _ in range(8)
            )
        else:
            # Modo Novo: Aleatório Sem Repetição
            possivel_solucao = "".join(random.sample(digitos_base, 8))

        resultado = verificar_oito_rainhas(possivel_solucao)
        dados.append(
            {"Possivel_Solucao": possivel_solucao, "Eh_Solucao": resultado}
        )

    return pd.DataFrame(dados)


def salvar_dataset(df: pd.DataFrame, nome_arquivo: str = "dataset.csv"):
    """Salva o DataFrame do Pandas em um arquivo CSV."""
    # index=False evita que o Pandas crie uma coluna extra com os índices numéricos
    df.to_csv(nome_arquivo, index=False)
    print(f"Dataset salvo com sucesso em: {nome_arquivo}")


# --- Exemplo de Uso ---

TAMANHO_DATASET = 1000
df_resultado = criar_dataset_alternado(TAMANHO_DATASET)
salvar_dataset(df_resultado, "dataset_oito_rainhas.csv")
