import random


def genetic_algorithm(criar_individuo, fitness, crossover, mutacao, tam_pop = 100, max_geracoes = 500, fitness_alvo = None, taxa_mutacao = 0.3, k = 3):
    def selection(pop):
        return max(random.sample(pop, k), key = fitness)
    
    pop = [criar_individuo() for _ in range(tam_pop)]
    
    for geracao in range(max_geracoes):
        
    