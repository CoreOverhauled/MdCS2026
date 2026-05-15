from matrix import Matrix, read_matrix_file, write_matrix_file, matrix
import sys

def reduce_column_down(m, k):
    for i in range(k + 1, m.nrows()):
        m.add_row(i, -m.get(i, k)/m.get(k, k), k)

def reduce_to_echelon(m):
    for i in range(0, m.nrows()):
        maxidx = i
        maxval = 0
        for j in range(i, m.nrows()):
            if abs(m.get(j,i)) > maxval:
                maxval = abs(m.get(j,i))
                maxidx = j
        m.swap_rows(i, maxidx)
        reduce_column_down(m, i)

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

if __name__ == "__main__":
    #g.err
    m1 = matrix([[1, 2, 3], [1, 2, 4]]) #sprzeczny
    reduce_to_echelon(m1)
    m1.eqs_print()
    m2 = matrix([[1, 0, 1], [2, 0, 2]]) #nieoznaczony
    reduce_to_echelon(m2)
    m2.eqs_print()
