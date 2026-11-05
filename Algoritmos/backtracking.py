def n_rainhas(n):
    solucoes = []
    colunas = set()
    diag1 = set()  
    diag2 = set() 
    tabuleiro = []

    def backtrack(linha):
        if linha == n:                       
            solucoes.append(tabuleiro[:])
            return

        for col in range(n):
            if col in colunas or (linha - col) in diag1 or (linha + col) in diag2:
                continue                    

            colunas.add(col); diag1.add(linha - col); diag2.add(linha + col)
            tabuleiro.append(col)

            backtrack(linha + 1)             

            
            tabuleiro.pop()
            colunas.remove(col); diag1.remove(linha - col); diag2.remove(linha + col)

    backtrack(0)
    return solucoes


from Algoritmos.resultado import ResultadoBusca


def resolver(n: int) -> ResultadoBusca:
    if n < 1:
        raise ValueError("N deve ser maior que zero.")

    colunas = set()
    diag1 = set()
    diag2 = set()
    tabuleiro = []
    estados_explorados = 0

    def backtrack(linha):
        nonlocal estados_explorados
        if linha == n:
            return True

        for col in range(n):
            if col in colunas or (linha - col) in diag1 or (linha + col) in diag2:
                continue

            estados_explorados += 1
            colunas.add(col)
            diag1.add(linha - col)
            diag2.add(linha + col)
            tabuleiro.append(col)

            if backtrack(linha + 1):
                return True

            tabuleiro.pop()
            colunas.remove(col)
            diag1.remove(linha - col)
            diag2.remove(linha + col)

        return False

    encontrado = backtrack(0)
    return ResultadoBusca(
        tabuleiro=tabuleiro[:] if encontrado else None,
        avaliacoes=1 if encontrado else 0,
        estados_explorados=estados_explorados
    )
