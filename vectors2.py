from vector_shower import show_vector, show_vector_cloud
from matrices import Matrix, matrix
import math

def vec2d(x, y):
    v = Matrix(2, 1)
    v.set(0, 0, x)
    v.set(1, 0, y)
    return v

def vmul(a, v):
    return vec2d(a * v.get(0, 0), a * v.get(1, 0))

def vadd(v1, v2):
    return vec2d(v1.get(0, 0) + v2.get(0, 0), v1.get(1, 0) + v2.get(1, 0))

def line(p0, p1):
    step = 0.001
    points = []
    t = 0
    while t * step < 1:
        points.append(vadd(vmul(t * step, p0), vmul(1-(t * step), p1)))
        t+=1
    return points

def circle(center, radius):
    step = 2 ** 6
    points = []
    for t in range(step, 0, -1):
        points += line(center, vadd(center, vec2d(radius * math.sin(math.radians((360.0 * t) / step)), radius * math.cos(math.radians((360.0 * t) / step)))))
    return points

def matmul(A, B):
    if A.ncols() != B.nrows():
        return None
    result = Matrix(A.nrows(), B.ncols())
    for i in range(A.nrows()):
        for j in range(B.ncols()):
            val = 0
            for n in range(A.ncols()):
                val += A.get(i, n) * B.get(n, j)
            result.set(i, j, val)
    return result

def transform(m, vs):
    return [matmul(m, v) for v in vs]

def mirror_y():
    return matrix([[1, 0], [0, -1]])

def rotate(angle):
    angle = math.radians(angle)
    return matrix([[math.cos(angle), math.sin(angle)], [-math.sin(angle), math.cos(angle)]])

if __name__ == "__main__":
    #show_vector_cloud(circle(vec2d(3, 3), 1))
    for i in transform(matrix([[1,2],[3,4]]),[vec2d(1,2), vec2d(5,-13371)]):
        if i != None:
            i.print_matrix()
    #rotate(30).print_matrix()