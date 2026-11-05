def verificar_oito_rainhas(solucao: str) -> bool:
    # 1. Validação de formato: deve ter exatamente 8 caracteres
    if len(solucao) != 8:
        return False

    # 2. Validação de conteúdo: todos devem ser dígitos de '1' a '8'
    if not all(c.isdigit() and '1' <= c <= '8' for c in solucao):
        return False

    # Converte a string para uma lista de inteiros (ajustando para índice 0 a 7)
    lines = [int(c) - 1 for c in solucao]

    # 3. Verifica ataques entre as rainhas
    for col1 in range(8):
        for col2 in range(col1 + 1, 8):
            lin1 = lines[col1]
            lin2 = lines[col2]

            # Verifica se estão na mesma linha
            if lin1 == lin2:
                return False

            # Verifica se estão na mesma diagonal
            # (A diferença entre as linhas é igual à diferença entre as colunas)
            if abs(lin1 - lin2) == abs(col1 - col2):
                return False

    return True


def contar_conflitos(tabuleiro: list[int] | tuple[int, ...]) -> int:
    n = len(tabuleiro)
    if n < 1 or any(type(linha) is not int or not 0 <= linha < n for linha in tabuleiro):
        raise ValueError("O tabuleiro deve conter linhas inteiras entre 0 e N-1.")

    conflitos = 0
    for i in range(n):
        for j in range(i + 1, n):
            if tabuleiro[i] == tabuleiro[j] or abs(tabuleiro[i] - tabuleiro[j]) == j - i:
                conflitos += 1
    return conflitos


def eh_solucao(tabuleiro: list[int] | tuple[int, ...]) -> bool:
    try:
        return contar_conflitos(tabuleiro) == 0
    except (TypeError, ValueError):
        return False
