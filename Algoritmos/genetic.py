import random

from Algoritmos.Verification import contar_conflitos
from Algoritmos.resultado import ResultadoBusca


def genetic_algorithm(
    criar_individuo, fitness, crossover, mutacao,
    tam_pop=100, max_geracoes=500, fitness_alvo=None,
    taxa_mutacao=0.3, k=3, taxa_cruzamento=1.0,
    elitismo=1, rng=None, on_generation=None
):
    if tam_pop < 2 or max_geracoes < 0:
        raise ValueError("População deve ter pelo menos 2 indivíduos e gerações não podem ser negativas.")
    if not 1 <= k <= tam_pop or not 1 <= elitismo < tam_pop:
        raise ValueError("Torneio e elitismo devem estar dentro dos limites da população.")
    if not 0 <= taxa_mutacao <= 1 or not 0 <= taxa_cruzamento <= 1:
        raise ValueError("As taxas devem estar entre 0 e 1.")

    rng = rng if rng is not None else random
    pop = [criar_individuo() for _ in range(tam_pop)]

    for geracao in range(max_geracoes + 1):
        pontuacoes = [fitness(individuo) for individuo in pop]
        ordem = sorted(range(tam_pop), key=lambda i: pontuacoes[i], reverse=True)
        melhor = pop[ordem[0]][:]
        melhor_fitness = pontuacoes[ordem[0]]

        if on_generation is not None:
            on_generation(geracao, melhor_fitness)

        if fitness_alvo is not None and melhor_fitness >= fitness_alvo:
            return melhor, geracao
        if geracao == max_geracoes:
            return melhor, geracao

        def selection():
            indices = rng.sample(range(tam_pop), k)
            return pop[max(indices, key=lambda i: pontuacoes[i])]

        nova_pop = [pop[i][:] for i in ordem[:elitismo]]
        while len(nova_pop) < tam_pop:
            pai1 = selection()
            pai2 = selection()
            filho = crossover(pai1, pai2) if rng.random() < taxa_cruzamento else pai1[:]
            if rng.random() < taxa_mutacao:
                filho = mutacao(filho)
            nova_pop.append(filho)
        pop = nova_pop


def cruzamento_ordenado(pai1: list[int], pai2: list[int], rng) -> list[int]:
    n = len(pai1)
    if n < 2:
        return pai1[:]

    inicio, fim = sorted(rng.sample(range(n), 2))
    filho = [None] * n
    filho[inicio:fim + 1] = pai1[inicio:fim + 1]
    posicao = (fim + 1) % n

    for i in range(n):
        gene = pai2[(fim + 1 + i) % n]
        if gene not in filho:
            filho[posicao] = gene
            posicao = (posicao + 1) % n
    return filho


def mutacao_troca(individuo: list[int], rng) -> list[int]:
    filho = individuo[:]
    if len(filho) > 1:
        i, j = rng.sample(range(len(filho)), 2)
        filho[i], filho[j] = filho[j], filho[i]
    return filho


def resolver(
    n: int, semente: int | None = None, tam_pop: int = 100,
    max_geracoes: int = 500, taxa_mutacao: float = 0.1,
    taxa_cruzamento: float = 0.8, k: int = 3, elitismo: int = 2
) -> ResultadoBusca:
    if n < 1:
        raise ValueError("N deve ser maior que zero.")

    rng = random.Random(semente)
    avaliacoes = 0
    historico = []
    fitness_alvo = n * (n - 1) // 2

    def criar_individuo():
        return rng.sample(range(n), n)

    def fitness(individuo):
        nonlocal avaliacoes
        avaliacoes += 1
        return fitness_alvo - contar_conflitos(individuo)

    def crossover(pai1, pai2):
        return cruzamento_ordenado(pai1, pai2, rng)

    def mutacao(individuo):
        return mutacao_troca(individuo, rng)

    def on_generation(geracao, melhor_fitness):
        historico.append(melhor_fitness)

    melhor, geracoes = genetic_algorithm(
        criar_individuo, fitness, crossover, mutacao,
        tam_pop=tam_pop, max_geracoes=max_geracoes,
        fitness_alvo=fitness_alvo, taxa_mutacao=taxa_mutacao,
        taxa_cruzamento=taxa_cruzamento, k=k, elitismo=elitismo,
        rng=rng, on_generation=on_generation
    )

    return ResultadoBusca(
        tabuleiro=melhor,
        avaliacoes=avaliacoes,
        geracoes=geracoes,
        historico_fitness=historico,
        limite_atingido=historico[-1] != fitness_alvo
    )
