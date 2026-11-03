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

print(len(n_rainhas(8)))  