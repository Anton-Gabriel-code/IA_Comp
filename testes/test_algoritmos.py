import random

import pytest

from Algoritmos import backtracking, bruteforce, genetic
from Algoritmos.Verification import eh_solucao
from Algoritmos.resultado import ResultadoBusca


@pytest.mark.parametrize("n", [1, 4, 8])
@pytest.mark.parametrize("resolver", [bruteforce.resolver, backtracking.resolver])
def test_buscas_deterministicas(n, resolver):
    resultado = resolver(n)
    assert isinstance(resultado, ResultadoBusca)
    assert eh_solucao(resultado.tabuleiro)
    assert resultado.avaliacoes >= 1


@pytest.mark.parametrize("n", [2, 3])
@pytest.mark.parametrize("resolver", [bruteforce.resolver, backtracking.resolver])
def test_sem_solucao(n, resolver):
    resultado = resolver(n)
    assert resultado.tabuleiro is None
    assert not resultado.limite_atingido


def test_backtracking_encontra_todas_as_92_solucoes():
    assert len(backtracking.n_rainhas(8)) == 92


def test_forca_bruta_respeita_limite():
    resultado = bruteforce.resolver(8, limite_avaliacoes=1)
    assert resultado.tabuleiro is None
    assert resultado.limite_atingido
    assert resultado.avaliacoes == 1


def test_genetico_reproduzivel():
    a = genetic.resolver(8, semente=42, tam_pop=40, max_geracoes=50)
    b = genetic.resolver(8, semente=42, tam_pop=40, max_geracoes=50)
    assert a == b
    assert isinstance(a.tabuleiro, list)
    assert sorted(a.tabuleiro) == list(range(8))
    assert a.avaliacoes >= 40
    assert len(a.historico_fitness) == a.geracoes + 1
    assert eh_solucao(a.tabuleiro) or a.limite_atingido


def test_operadores_geneticos_preservam_permutacoes():
    pai1 = list(range(8))
    pai2 = list(reversed(range(8)))
    for semente in range(100):
        rng = random.Random(semente)
        filho = genetic.cruzamento_ordenado(pai1, pai2, rng)
        mutante = genetic.mutacao_troca(filho, rng)
        assert sorted(filho) == pai1
        assert sorted(mutante) == pai1
        assert pai1 == list(range(8))


def test_parametros_invalidos():
    with pytest.raises(ValueError):
        genetic.resolver(8, tam_pop=1)
    with pytest.raises(ValueError):
        genetic.resolver(8, taxa_mutacao=1.5)
    with pytest.raises(ValueError):
        backtracking.resolver(0)
