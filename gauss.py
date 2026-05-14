from matrices import Matrix
import sys

def reduce_column_down(m: Matrix, k):
    for i in range(k + 1, m.rows):
        m.add_row(i, -(m.get(i, k) / m.get(k, k)), k)
    
def reduce_to_echelon(m: Matrix):
    for i in range(min(m.nrows(), m.ncols() - 1)):
        max_row = i
        for j in range(i, m.nrows()):
            if abs(m.get(j, i)) > abs(m.get(max_row, i)):
                max_row = j
        m.swap_rows(i, max_row)
        reduce_column_down(m, i)

def extend_solution(m: Matrix, k, x):
    rhs = m.get(k, m.ncols() - 1)
    for i in range(k + 1 , m.nrows()):
        print(i)
        rhs -= m.get(k, i) * x[i]
    rhs /= m.get(k, k)
    return rhs

def compute_solution(echelon_m):
    ... # TODO: funkcja wyliczająca rozwiązanie z wyschodkowanej macierzy

if __name__ == '__main__':
    # m = Matrix(3, 3)
    # m.set_whole([[1,2,3],[4,5,6],[7,8,9]])
    # reduce_to_echelon(m)
    # print(m)
    m = Matrix(3, 4)
    m.set(0, 0, 1); m.set(0, 1, 5); m.set(0, 2, 4); m.set(0, 3, 9)
    m.set(1, 1, 1); m.set(1, 2, -3); m.set(1, 3, 2)
    m.set(2, 2, 1); m.set(2, 3, -1)
    sol = [None] * 3  # Na początek nie znamy żadnej z trzech zmiennych
    sol[2] = extend_solution(m, 2, sol)
    sol[1] = extend_solution(m, 1, sol)
    sol[0] = extend_solution(m, 0, sol)
    if sol == [18, -1, -1]:
        print("extend_solution: OK")
    else:
        print("extend_solution: ERROR")