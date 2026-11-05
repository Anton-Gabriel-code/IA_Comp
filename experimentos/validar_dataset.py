from pathlib import Path

import pandas as pd

from Algoritmos.Verification import verificar_oito_rainhas


ARQUIVO_PADRAO = Path(__file__).resolve().parents[1] / "Dataset" / "dataset_oito_rainhas_1000_soluções.csv"


def validar_dataset(arquivo: str | Path = ARQUIVO_PADRAO) -> dict[str, int]:
    dados = pd.read_csv(arquivo, dtype={"Possivel_Solucao": str})
    colunas = {"Possivel_Solucao", "Eh_Solucao"}
    if not colunas.issubset(dados.columns):
        raise ValueError("O dataset deve conter as colunas Possivel_Solucao e Eh_Solucao.")

    rotulos = dados["Eh_Solucao"].astype(str).str.strip().str.lower()
    if not rotulos.isin(["true", "false"]).all():
        raise ValueError("A coluna Eh_Solucao deve conter somente True ou False.")

    verificacoes = dados["Possivel_Solucao"].apply(verificar_oito_rainhas)
    classificacoes = rotulos == "true"
    return {
        "registros": len(dados),
        "configuracoes_distintas": dados["Possivel_Solucao"].nunique(),
        "solucoes_validas": int(verificacoes.sum()),
        "solucoes_invalidas": int((~verificacoes).sum()),
        "divergencias": int((verificacoes != classificacoes).sum()),
    }
