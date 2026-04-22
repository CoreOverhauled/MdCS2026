import math
class Matrix:
    def __init__(self, rows, cols):
        self._data = [[0 for a in range(0, cols)] for b in range(0, rows)]

    def get(self, row, col):
        if not (0 <= row < self.nrows() and 0 <= col < self.ncols()):
            raise IndexError(f"Niepoprawny index ({row}, {col}) w macierzy o wymiarach {self.nrows()}x{self.ncols()}")
        return self._data[row][col]

    def set(self, row, col, val):
        if not (0 <= row < self.nrows() and 0 <= col < self.ncols()):
            raise IndexError(f"Niepoprawny index ({row}, {col}) w macierzy o wymiarach {self.nrows()}x{self.ncols()}")
        self._data[row][col] = val

    def nrows(self):
        return len(self._data)

    def ncols(self):
        return len(self._data[0])

    def swap_rows(self, row1, row2):
        temp = self._data[row1]
        self._data[row1] = self._data[row2]
        self._data[row2] = temp

    def multiply(self, row, scalar):
        self._data[row] = [x * scalar for x in self._data[row]]

    def add_row(self, dst_row, scalar, src_row):
        self._data[dst_row] = [(self._data[dst_row][x] + scalar * self._data[src_row][x])
                              for x in range(0, len(self._data[dst_row]))]

    def eqs_print(self):
        for a in self._data:
            PrintedAny = False
            for i in range(0, len(a)):
                if i == len(a) - 1:
                    if not PrintedAny:
                        continue
                    print(f" = {a[i]}")
                    continue
                if a[i] == 0:
                    continue
                if PrintedAny:
                    if a[i] == 1:
                        print(f" + x{i + 1}", end = '')
                    elif a[i] < 0:
                        print(f" - {-a[i]}*x{i + 1}", end = '')
                    else:
                        print(f" + {a[i]}*x{i + 1}", end = '')
                else:
                    PrintedAny = True
                    if a[i] == 1:
                        print(f"x{i + 1}", end = '')
                    else:
                        print(f"{a[i]}*x{i + 1}", end = '')
    
    def max_abs(self):
        return max([max([abs(x) for x in row]) for row in self._data])
    def check_solution(self, xs):
        SatisfiesEquations = True
        maxvalue = self.max_abs()
        for row in self._data:
            lhs = 0
            for i in range(0, len(row)-1):
                lhs += row[i] * xs[i]
            SatisfiesEquations &= (abs(lhs - row[-1]) < 1e-6 * maxvalue)
        return SatisfiesEquations


def read_matrix_file(filename):
    number_of_columns = None
    number_of_rows = 0
    elements = []
    with open(filename, "rb") as opened_file:
        for lineno, line in enumerate(opened_file):
            line_elements = line.split()
            if not line_elements:
                continue
            number_of_rows += 1
            if number_of_columns is None:
                number_of_columns = len(line_elements)
            else:
                if len(line_elements) != number_of_columns:
                    raise ValueError(f"{filename}:{lineno}: zla liczba elementow"
                        f" - {len(line_elements)} zamiast {number_of_columns}")
            for element in line_elements:
                try:
                    elements.append(float(element))
                except ValueError:
                    raise ValueError(f"{filename}:{lineno}: niepoprawna liczba '{element}'")
    result = Matrix(number_of_rows, number_of_columns)
    elements.reverse()
    for r in range(number_of_rows):
        for c in range(number_of_columns):
            result.set(r, c, elements.pop())
    return result

def write_matrix_file(filename, matrix):
    sizes = [0] * matrix.ncols()
    for r in range(matrix.nrows()):
        for c in range(matrix.ncols()):
            sizes[c] = max(sizes[c], len(str(matrix.get(r, c))))
    with open(filename, "w") as opened_file:
        for r in range(matrix.nrows()):
            for c in range(matrix.ncols()):
                if c == 0:
                    opened_file.write("  ")
                opened_file.write(str(matrix.get(r, c)))
            opened_file.write("\n")

def rotate_2d(alpha):
    rotmatrix = Matrix(2, 2)
    rotmatrix.set(0, 0, math.cos(alpha)); rotmatrix.set(0, 1, -math.sin(alpha))
    rotmatrix.set(1, 0, math.sin(alpha)); rotmatrix.set(1, 1, math.cos(alpha))
    return rotmatrix

def invert_2x2(m1):
    invm1 = Matrix(2, 2)
    detm1 = m1.get(0, 0) * m1.get(1, 1) - m1.get(0, 1) * m1.get(1, 0)
    invm1.set(0, 0, m1.get(1, 1)/detm1); invm1.set(0, 1, -m1.get(0, 1)/detm1)
    invm1.set(1, 0, -m1.get(1, 0)/detm1); invm1.set(1, 1, m1.get(0, 0)/detm1)
    return invm1




m = Matrix(5, 6)
# Wiersz 0
m.set(0, 0, 0); m.set(0, 1, 1); m.set(0, 2, 1); m.set(0, 3, 1); m.set(0, 4, 1); m.set(0, 5, 14)
# Wiersz 1
m.set(1, 0, 1); m.set(1, 1, 1); m.set(1, 2, 1); m.set(1, 3, 1); m.set(1, 4, 1); m.set(1, 5, 15)
# Wiersz 2
m.set(2, 0, 1); m.set(2, 1, 1); m.set(2, 2, 2); m.set(2, 3, 2); m.set(2, 4, 2); m.set(2, 5, 27)
# Wiersz 3
m.set(3, 0, 1); m.set(3, 1, 1); m.set(3, 2, 2); m.set(3, 3, 3); m.set(3, 4, 3); m.set(3, 5, 36)
# Wiersz 4
m.set(4, 0, 1); m.set(4, 1, 1); m.set(4, 2, 2); m.set(4, 3, 3); m.set(4, 4, 4); m.set(4, 5, 41)


#zadanie m.eqs
m.swap_rows(0, 1)
m.add_row(0, -1, 1)
m.add_row(2, -1, 0)
m.add_row(3, -1, 0)
m.add_row(4, -1, 0)
m.add_row(2, -1, 1)
m.add_row(3, -1, 1)
m.add_row(4, -1, 1)
m.add_row(1, -1, 2)
m.add_row(3, -1, 2)
m.add_row(4, -1, 2)
m.add_row(2, -1, 3)
m.add_row(4, -1, 3)
m.add_row(3, -1, 4)
m.eqs_print()

