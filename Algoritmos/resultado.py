from dataclasses import dataclass, field


@dataclass
class ResultadoBusca:
    tabuleiro: list[int] | None
    avaliacoes: int
    estados_explorados: int = 0
    geracoes: int = 0
    historico_fitness: list[int] = field(default_factory=list)
    limite_atingido: bool = False
