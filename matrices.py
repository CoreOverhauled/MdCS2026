from math import radians, sin, cos

class Matrix:
    def __init__(self, rows, cols):
        self._data = [[0 for _ in range(cols)] for _ in range(rows)]
        self.cols = cols
        self.rows = rows

    def nrows(self):
        return self.rows

    def ncols(self):
        return self.cols

    def get(self, row, col):
        if not (0 <= row < self.nrows() and 0 <= col < self.ncols()):
            raise IndexError(f"Niepoprawny index ({row}, {col}) w macierzy o wymiarach {self.nrows()}x{self.ncols()}")
        return self._data[row][col]

    def set(self, row, col, val):
        if not (0 <= row < self.nrows() and 0 <= col < self.ncols()):
            raise IndexError(f"Niepoprawny index ({row}, {col}) w macierzy o wymiarach {self.nrows()}x{self.ncols()}")
        self._data[row][col] = val

    def set_whole(self, val: list[list[int | float]]):
        if len(val) != self.rows:
            raise ValueError(f"Oczekiwano {self.rows} wierszy, otrzymano {len(val)}")
        if any(len(row) != self.cols for row in val):
            raise ValueError(f"Oczekiwano {self.cols} kolumn w każdym wierszu")
        self._data = val

    def swap_rows(self, row1, row2):
        self._data[row1], self._data[row2] = self._data[row2], self._data[row1]

    def multiply_row(self, row, n):
        self._data[row] = [num * n for num in self._data[row]]

    def add_row(self, row1, n, row2):
        self._data[row1] = [round(num1 + n * num2, 3) for num1, num2 in zip(self._data[row1], self._data[row2])]

    def eqs_print(self):
        num_vars = self.ncols() - 1
        for row in range(self.nrows()):
            terms = []
            for col in range(num_vars):
                num, var = self.get(row, col), f"x{col + 1}"
                if num == 0: continue
                terms.append(f"{'-' if num == -1 else '' if num == 1 else f'{num}*'}{var}")

            left_side = terms[0] if terms else "0"
            for term in terms[1:]:
                left_side += f" - {term[1:]}" if term.startswith("-") else f" + {term}"
            print(f"{left_side} = {self.get(row, num_vars)}")

    def check_solution(self, xs): #ZAD m.check2
        error = 1e-6 * max(abs(self._data[row][col]) for row in range(self.nrows()) for col in range(self.ncols()))
        for row in range(self.nrows()):
            left_side = sum(self.get(row, col) * xs[row] for col in range(self.ncols()))
            right_side = self.get(row, self.ncols() - 1)
            if abs(left_side - right_side) > error:
                return False
        return True
    
    def print_matrix(self):
        for i in self._data:
            print("|", end = " ")
            for j in i:
                print(j, end = " ")
            print("|")


    def __str__(self):
        return str(self._data)

def read_matrix_file(filename):
    number_of_columns = None
    number_of_rows = 0
    elements = []
    with open(filename) as opened_file:
        for lineno, line in enumerate(opened_file):
            line_elements = line.split()
            if not line_elements:
                continue
            number_of_rows += 1
            if number_of_columns is None:
                number_of_columns = len(line_elements)
            else:
                if len(line_elements) != number_of_columns:
                    raise ValueError(f"{filename}:{lineno}: zła liczba elementów"
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


def write_matrix_file(matrix, filename=None):
    sizes = [0] * matrix.ncols()
    for r in range(matrix.nrows()):
        for c in range(matrix.ncols()):
            sizes[c] = max(sizes[c], len(str(matrix.get(r, c))))
    if filename:
        opened_file = open(filename, "w")
    else:
        from sys import stdout
        opened_file = stdout
    for r in range(matrix.nrows()):
        for c in range(matrix.ncols()):
            if c != 0:
                opened_file.write("  ")
            opened_file.write(str(matrix.get(r, c)).rjust(sizes[c]))
        opened_file.write("\n")
    if filename:
        opened_file.close()

def matrix(data):
    m = Matrix(len(data), len(data[0]))
    for i in range(len(data)):
        for j in range(len(data[0])):
            m.set(i,j,data[i][j])
    return m

def rotate_2d(alpha): #ZAD m.rotate
    alpha = radians(alpha)
    matrix = Matrix(2, 2)
    matrix.set_whole([[cos(alpha), -sin(alpha)], [sin(alpha), cos(alpha)]])
    return matrix
if __name__ == '__main__':
    #ZAD m.eqs
    m = Matrix(5, 6)
    m.set(0, 0, 0); m.set(0, 1, 1); m.set(0, 2, 1); m.set(0, 3, 1); m.set(0, 4, 1); m.set(0, 5, 14)
    # Wiersz 1
    m.set(1, 0, 1); m.set(1, 1, 1); m.set(1, 2, 1); m.set(1, 3, 1); m.set(1, 4, 1); m.set(1, 5, 15)
    # Wiersz 2
    m.set(2, 0, 1); m.set(2, 1, 1); m.set(2, 2, 2); m.set(2, 3, 2); m.set(2, 4, 2); m.set(2, 5, 27)
    # Wiersz 3
    m.set(3, 0, 1); m.set(3, 1, 1); m.set(3, 2, 2); m.set(3, 3, 3); m.set(3, 4, 3); m.set(3, 5, 36)
    # Wiersz 4
    m.set(4, 0, 1); m.set(4, 1, 1); m.set(4, 2, 2); m.set(4, 3, 3); m.set(4, 4, 4); m.set(4, 5, 41)

    m.swap_rows(0, 1)

    m.add_row(2, -1, 0)
    m.add_row(3, -1, 0)
    m.add_row(4, -1, 0)

    m.add_row(3, -1, 2)
    m.add_row(4, -1, 2)

    m.add_row(4, -1, 3)

    m.eqs_print()