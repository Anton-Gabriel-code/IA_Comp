from pathlib import Path
from time import perf_counter_ns

import pandas as pd

from Algoritmos import backtracking, bruteforce, genetic
from Algoritmos.Verification import contar_conflitos, eh_solucao


ALGORITMOS = {
    "forca_bruta": bruteforce.resolver,
    "backtracking": backtracking.resolver,
    "genetico": genetic.resolver,
}


def executar_algoritmo(nome: str, n: int, iteracao: int = 1, **parametros):
    if nome not in ALGORITMOS:
        raise ValueError(f"Algoritmo desconhecido: {nome}")

    inicio = perf_counter_ns()
    resultado = ALGORITMOS[nome](n=n, **parametros)
    tempo_ms = (perf_counter_ns() - inicio) / 1_000_000
    tabuleiro = resultado.tabuleiro

    registro = {
        "algoritmo": nome,
        "n": n,
        "iteracao": iteracao,
        "semente": parametros.get("semente"),
        "tempo_ms": tempo_ms,
        "avaliacoes": resultado.avaliacoes,
        "estados_explorados": resultado.estados_explorados,
        "geracoes": resultado.geracoes,
        "sucesso": tabuleiro is not None and eh_solucao(tabuleiro),
        "conflitos": contar_conflitos(tabuleiro) if tabuleiro is not None else None,
        "limite_atingido": resultado.limite_atingido,
        "tabuleiro": "-".join(map(str, tabuleiro)) if tabuleiro is not None else "",
    }
    evolucao = [
        {
            "algoritmo": nome,
            "n": n,
            "iteracao": iteracao,
            "semente": parametros.get("semente"),
            "geracao": geracao,
            "melhor_fitness": fitness,
        }
        for geracao, fitness in enumerate(resultado.historico_fitness)
    ]
    return registro, evolucao


def executar_experimentos(
    algoritmos: list[str], n: int = 8, repeticoes: int = 30,
    semente: int = 42, limite_avaliacoes: int = 1_000_000,
    tam_pop: int = 100, max_geracoes: int = 500,
    taxa_mutacao: float = 0.1, taxa_cruzamento: float = 0.8,
    k: int = 3, elitismo: int = 2
):
    if n < 1 or repeticoes < 1:
        raise ValueError("N e repetições devem ser positivos.")

    registros = []
    historicos = []
    for nome in algoritmos:
        for iteracao in range(1, repeticoes + 1):
            parametros = {}
            if nome == "forca_bruta":
                parametros["limite_avaliacoes"] = limite_avaliacoes
            if nome == "genetico":
                parametros = {
                    "semente": semente + iteracao - 1,
                    "tam_pop": tam_pop,
                    "max_geracoes": max_geracoes,
                    "taxa_mutacao": taxa_mutacao,
                    "taxa_cruzamento": taxa_cruzamento,
                    "k": k,
                    "elitismo": elitismo,
                }

            registro, evolucao = executar_algoritmo(nome, n, iteracao, **parametros)
            registros.append(registro)
            historicos.extend(evolucao)

    return pd.DataFrame(registros), pd.DataFrame(historicos)


def resumir_resultados(execucoes: pd.DataFrame) -> pd.DataFrame:
    return (
        execucoes.groupby(["algoritmo", "n"], as_index=False)
        .agg(
            execucoes=("sucesso", "size"),
            taxa_sucesso=("sucesso", "mean"),
            tempo_mediano_ms=("tempo_ms", "median"),
            tempo_medio_ms=("tempo_ms", "mean"),
            desvio_tempo_ms=("tempo_ms", "std"),
            avaliacoes_medias=("avaliacoes", "mean"),
            estados_medios=("estados_explorados", "mean"),
            geracoes_medias=("geracoes", "mean"),
            conflitos_medios=("conflitos", "mean"),
        )
        .assign(taxa_sucesso=lambda dados: dados["taxa_sucesso"] * 100)
    )


def salvar_resultados(execucoes: pd.DataFrame, evolucao: pd.DataFrame, pasta: str | Path):
    destino = Path(pasta)
    destino.mkdir(parents=True, exist_ok=True)
    execucoes.to_csv(destino / "execucoes.csv", index=False)
    resumo = resumir_resultados(execucoes)
    resumo.to_csv(destino / "resumo.csv", index=False)
    caminho_evolucao = destino / "evolucao_genetico.csv"
    if not evolucao.empty:
        evolucao.to_csv(caminho_evolucao, index=False)
    elif caminho_evolucao.exists():
        caminho_evolucao.unlink()
    return resumo
