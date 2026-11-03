import random


def genetic_algorithm(criar_individuo, fitness, crossover, mutacao, tam_pop = 100, max_geracoes = 500, fitness_alvo = None, taxa_mutacao = 0.3, k = 3):
    def selection(pop):
        return max(random.sample(pop, k), key = fitness)
    
    pop = [criar_individuo() for _ in range(tam_pop)]
    
    for geracao in range(max_geracoes):
        melhor = max(pop, key=fitness)
        if fitness_alvo is not None and fitness(melhor) >= fitness_alvo:
            return melhor, geracao
        
        
        nova_pop = [melhor]
        while len(nova_pop) < tam_pop:
            filho = crossover(selection(pop), selection(pop))
            if random.random() < taxa_mutacao:
                filho = mutacao(filho)
            nova_pop.append(filho)
        pop = nova_pop
        
    return max(pop, key = fitness), max_geracoes