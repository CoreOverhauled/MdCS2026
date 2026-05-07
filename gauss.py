from matrix import Matrix, read_matrix_file, write_matrix_file, matrix
import sys

def reduce_column_down(m, k):
    for i in range(k, m.ncols()):
        m.add_row(i, -m.get(i-1, k-1)/m.get(k-1, k-1), k - 1)

def reduce_to_echelon(m):
    ... # TODO: funkcja schodkująca macierze

def extend_solution(m, k, x):
    n = m.nrows()
    x_k = m.get(k, n)
    for i in range(k + 1, n):
        x_k -= m.get(k, i) * x[i]
    x_k /= m.get(k, k)
    return x_k

def compute_solution(echelon_m):
    sol=[None] * echelon_m.nrows()
    for i in range(echelon_m.nrows()-1, -1, -1):
        sol[i] = extend_solution(echelon_m, i, sol)
    return sol

if __name__ == "__main__": #and len(sys.argv) >= 2:
    #m = read_matrix_file(sys.argv[1])
    #reduce_to_echelon(m)
    #sol = compute_solution(m)
    #print(f"Rozwiązanie: {sol}")
    #if len(sys.argv) >= 3:
    #    write_matrix_file(m, sys.argv[2])
    m = Matrix(3, 4)
    m.set(0, 0, 1); m.set(0, 1, 5); m.set(0, 2, 4); m.set(0, 3, 9)
    m.set(1, 1, 1); m.set(1, 2, -3); m.set(1, 3, 2)
    m.set(2, 2, 1); m.set(2, 3, -1)
    sol = [None] * 3  # Na początek nie znamy żadnej z trzech zmiennych
    sol[2] = extend_solution(m, 2, sol)
    sol[1] = extend_solution(m, 1, sol)
    sol[0] = extend_solution(m, 0, sol)
    #if sol == [18, -1, -1]:
    #    print("extend_solution: OK")
    #else:
    #    print("extend_solution: ERROR")
    #    print(sol)
    print(compute_solution(matrix(8, 9, [[1, 2, -1, 3, 0, 1, 4, -2, 5],
                                        [0, 1, 3, -2, 1, 4, 0, 1, 12],
                                        [0, 0, 1, 5, -3, 2, 1, 3, -4],
                                        [0, 0, 0, 1, 4, -1, 2, 2, 7],
                                        [0, 0, 0, 0, 1, 3, 0, -1, 0],
                                        [0, 0, 0, 0, 0, 1, 5, 4, 9],
                                        [0, 0, 0, 0, 0, 0, 1, -3, 2],
                                        [0, 0, 0, 0, 0, 0, 0, 1, -1]])))