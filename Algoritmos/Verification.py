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
