from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def _grafico_barras(dados, coluna, titulo, eixo_y, caminho):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(dados["algoritmo"], dados[coluna])
    ax.set_title(titulo)
    ax.set_ylabel(eixo_y)
    ax.set_xlabel("Algoritmo")
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close(fig)


def gerar_graficos(pasta: str | Path) -> list[Path]:
    pasta = Path(pasta)
    resumo = pd.read_csv(pasta / "resumo.csv")
    arquivos = []

    definicoes = [
        ("tempo_mediano_ms", "Tempo mediano de execução", "Tempo (ms)", "tempo_execucao.png"),
        ("avaliacoes_medias", "Avaliações completas ou de fitness", "Avaliações", "avaliacoes.png"),
        ("taxa_sucesso", "Taxa de sucesso", "Sucesso (%)", "taxa_sucesso.png"),
    ]
    for coluna, titulo, eixo_y, nome_arquivo in definicoes:
        caminho = pasta / nome_arquivo
        _grafico_barras(resumo, coluna, titulo, eixo_y, caminho)
        arquivos.append(caminho)

    caminho_evolucao = pasta / "evolucao_genetico.csv"
    if caminho_evolucao.exists():
        evolucao = pd.read_csv(caminho_evolucao)
        if not evolucao.empty:
            primeira = evolucao[evolucao["iteracao"] == evolucao["iteracao"].min()]
            primeira = primeira.sort_values("geracao")
            fig, ax = plt.subplots(figsize=(8, 4.5))
            ax.plot(primeira["geracao"], primeira["melhor_fitness"], marker="o")
            ax.set_title("Evolução do melhor fitness na primeira execução")
            ax.set_xlabel("Geração")
            ax.set_ylabel("Fitness")
            ax.grid(alpha=0.2)
            fig.tight_layout()
            caminho = pasta / "evolucao_genetico.png"
            fig.savefig(caminho, dpi=150)
            plt.close(fig)
            arquivos.append(caminho)

    else:
        caminho_antigo = pasta / "evolucao_genetico.png"
        if caminho_antigo.exists():
            caminho_antigo.unlink()

    return arquivos
