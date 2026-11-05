import pandas as pd

from experimentos.executar import executar_experimentos, salvar_resultados
from experimentos.graficos import gerar_graficos


def test_experimentos_e_exportacao(tmp_path):
    dados, evolucao = executar_experimentos(
        algoritmos=["forca_bruta", "backtracking", "genetico"],
        n=4, repeticoes=2, semente=42,
        tam_pop=20, max_geracoes=15
    )
    assert len(dados) == 6
    assert dados["sucesso"].isin([True, False]).all()
    assert not evolucao.empty

    resumo = salvar_resultados(dados, evolucao, tmp_path)
    assert len(resumo) == 3
    assert (tmp_path / "execucoes.csv").exists()
    assert (tmp_path / "resumo.csv").exists()
    assert (tmp_path / "evolucao_genetico.csv").exists()
    assert len(pd.read_csv(tmp_path / "execucoes.csv")) == 6

    graficos = gerar_graficos(tmp_path)
    assert len(graficos) == 4
    assert all(caminho.stat().st_size > 0 for caminho in graficos)
