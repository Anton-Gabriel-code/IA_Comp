import pytest

from Algoritmos.Verification import contar_conflitos, eh_solucao, verificar_oito_rainhas
from experimentos.validar_dataset import validar_dataset


def test_solucao_valida():
    assert eh_solucao([0, 4, 7, 5, 2, 6, 1, 3])
    assert verificar_oito_rainhas("15863724")


def test_conflitos_mesma_linha():
    assert contar_conflitos([0] * 8) == 28


def test_conflitos_mesma_diagonal():
    assert contar_conflitos(list(range(8))) == 28


def test_posicao_invalida():
    assert not eh_solucao([0, 4, 7, 5, 2, 6, 1, 8])
    assert not verificar_oito_rainhas("01234567")
    assert not verificar_oito_rainhas("92345678")


def test_contagem_rejeita_dados_invalidos():
    with pytest.raises(ValueError):
        contar_conflitos([0, 1, 9])


def test_dataset_original():
    resumo = validar_dataset()
    assert resumo["registros"] == 1000
    assert resumo["configuracoes_distintas"] == 998
    assert resumo["solucoes_validas"] == 3
    assert resumo["divergencias"] == 0
