import random
from itertools import permutations

import pandas as pd

from Algoritmos.Verification import contar_conflitos, verificar_oito_rainhas
from Algoritmos.resultado import ResultadoBusca


def forca_bruta_ruim(tamanho: int) -> pd.DataFrame:
    dados = []
    for _ in range(tamanho):
        possivel_solucao = "".join(str(random.randint(1, 8)) for _ in range(8))
        resultado = verificar_oito_rainhas(possivel_solucao)
        dados.append({"Possivel_Solucao": possivel_solucao, "Eh_Solucao": resultado})
    return pd.DataFrame(dados)


def forca_bruta_melhor(tamanho: int) -> pd.DataFrame:
    dados = []
    digitos_base = ["1", "2", "3", "4", "5", "6", "7", "8"]
    for _ in range(tamanho):
        possivel_solucao = "".join(random.sample(digitos_base, 8))
        resultado = verificar_oito_rainhas(possivel_solucao)
        dados.append({"Possivel_Solucao": possivel_solucao, "Eh_Solucao": resultado})
    return pd.DataFrame(dados)


def resolver(n: int, limite_avaliacoes: int | None = 1_000_000) -> ResultadoBusca:
    if n < 1:
        raise ValueError("N deve ser maior que zero.")
    if limite_avaliacoes is not None and limite_avaliacoes < 1:
        raise ValueError("O limite de avaliações deve ser positivo.")

    avaliacoes = 0
    for configuracao in permutations(range(n)):
        if limite_avaliacoes is not None and avaliacoes >= limite_avaliacoes:
            return ResultadoBusca(None, avaliacoes, limite_atingido=True)

        avaliacoes += 1
        if contar_conflitos(configuracao) == 0:
            return ResultadoBusca(list(configuracao), avaliacoes)

    return ResultadoBusca(None, avaliacoes)
