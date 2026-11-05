import argparse
from pathlib import Path

from experimentos.executar import executar_experimentos, salvar_resultados
from experimentos.graficos import gerar_graficos
from experimentos.validar_dataset import validar_dataset


def main():
    parser = argparse.ArgumentParser(description="Comparação de algoritmos para o problema das N rainhas")
    parser.add_argument("--algoritmo", choices=["todos", "forca_bruta", "backtracking", "genetico"], default="todos")
    parser.add_argument("--n", type=int, default=8)
    parser.add_argument("--repeticoes", type=int, default=None)
    parser.add_argument("--semente", type=int, default=42)
    parser.add_argument("--populacao", type=int, default=100)
    parser.add_argument("--geracoes", type=int, default=500)
    parser.add_argument("--mutacao", type=float, default=0.1)
    parser.add_argument("--cruzamento", type=float, default=0.8)
    parser.add_argument("--torneio", type=int, default=3)
    parser.add_argument("--elitismo", type=int, default=2)
    parser.add_argument("--limite-avaliacoes", type=int, default=1_000_000)
    parser.add_argument("--saida", type=Path, default=Path("resultados"))
    parser.add_argument("--sem-graficos", action="store_true")
    parser.add_argument("--validar-dataset", action="store_true")
    args = parser.parse_args()

    if args.validar_dataset:
        for chave, valor in validar_dataset().items():
            print(f"{chave}: {valor}")
        return

    algoritmos = ["forca_bruta", "backtracking", "genetico"] if args.algoritmo == "todos" else [args.algoritmo]
    repeticoes = args.repeticoes if args.repeticoes is not None else (30 if args.algoritmo == "todos" else 1)

    try:
        execucoes, evolucao = executar_experimentos(
            algoritmos=algoritmos, n=args.n, repeticoes=repeticoes,
            semente=args.semente, limite_avaliacoes=args.limite_avaliacoes,
            tam_pop=args.populacao, max_geracoes=args.geracoes,
            taxa_mutacao=args.mutacao, taxa_cruzamento=args.cruzamento,
            k=args.torneio, elitismo=args.elitismo
        )
    except ValueError as erro:
        parser.error(str(erro))

    resumo = salvar_resultados(execucoes, evolucao, args.saida)
    print(resumo.round(3).to_string(index=False))
    print(f"Resultados: {args.saida.resolve()}")
    if not args.sem_graficos:
        for caminho in gerar_graficos(args.saida):
            print(f"Gráfico: {caminho}")


if __name__ == "__main__":
    main()
