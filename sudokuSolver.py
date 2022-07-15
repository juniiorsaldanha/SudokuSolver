import pycosat
import sys, getopt
import numpy as np #printar o sudoku
     
def v(i, j, digito): 
    return 81 * (i - 1) + 9 * (j - 1) + digito

#Reduzir o problema para clausulas SAT 
def sudoku_clauses(): 
    res = []
    #Determinar que todos os quadradinhos tenha somente números de 1 até 9 
    #e que não tenha dois números repetidos
    for i in range(1, 10):
        for j in range(1, 10):
            res.append([v(i, j, digito) for digito in range(1, 10)])
            for digito in range(1, 10):
                for dp in range(digito + 1, 10):
                    res.append([-v(i, j, digito), -v(i, j, dp)])

    def validar(quadrados): 
        for i, xi in enumerate(quadrados):
            for j, xj in enumerate(quadrados):
                if i < j:
                    for d in range(1, 10):
                        res.append([-v(xi[0], xi[1], d), -v(xj[0], xj[1], d)])

    # Verificar que linhas e colunas terão números diferentes 
    for i in range(1, 10):
        validar([(i, j) for j in range(1, 10)])
        validar([(j, i) for j in range(1, 10)])
        
    # Verificar que quadradinhos terão números diferentes
    for i in 1, 4, 7:
        for j in 1, 4 ,7:
            validar([(i + k % 3, j + k // 3) for k in range(9)])
      
    return res

def solve(matrix):
    print('Problema Sudoku: ')
    print(np.matrix(matrix))
    clauses = sudoku_clauses()
    for i in range(1, 10):
        for j in range(1, 10):
            digito = matrix[i - 1][j - 1] 
            if digito:
                clauses.append([v(i, j, digito)])
    
    # Resolver o problema SAT
    sol = set(pycosat.solve(clauses))
    
    def ler_matrix(i, j):
        # Retorna o digito, de acordo com a solução SAT
        for digito in range(1, 10):
            if v(i, j, digito) in sol:
                return digito

    for i in range(1, 10):
        for j in range(1, 10):
            matrix[i - 1][j - 1] = ler_matrix(i, j)
    print('Problema Resolvido: ')
    print(np.matrix(matrix))


if __name__ == '__main__':

    # Problema Sudoku do trabalho 

    matrix = [[5,3,0,0,7,0,0,0,0],
            [6,0,0,1,9,5,0,0,0],
            [0,9,8,0,0,0,0,6,0],
            [8,0,0,0,6,0,0,0,3],
            [4,0,0,8,0,3,0,0,1],
            [7,0,0,0,2,0,0,0,6],
            [0,6,0,0,0,0,2,8,0],
            [0,0,0,4,1,9,0,0,5],
            [0,0,0,0,8,0,0,7,9]]
    
    solve(matrix)