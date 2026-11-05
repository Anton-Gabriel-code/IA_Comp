
from dataclasses import dataclass


@dataclass
class ResultadoBusca:
    tabuleiro: list[int] | None
    avaliacoes: int
    estados_explorados: int = 0
    geracoes: int = 0
    historico_fitness: list[int] | None = None
