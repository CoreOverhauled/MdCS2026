import math
class Vector2D:
    def __init__(self, name):
        # To jest komentarz. Mozesz w dowolym miejscu wstawic linijke zaczynajaca sie od #
        # i napisac tak cokolwiek.
        # To dobry sposob na robienie notatek!
        self.x = 0.0
        self.y = 0.0
        self.name = name

    def add(self, other_vector):
        self.x = self.x + other_vector.x
        self.y = self.y + other_vector.y

    def multiply(self, scale):
        self.x *= scale
        self.y *= scale

    def show(self):
        print(f"Wektor {self.name}=({self.x}, {self.y})")

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

def lid2d(v1, v2):
    return v1.x * v2.y - v1.y * v2.x != 0


def XY(x, y):
    new_vec = Vector2D("v")
    new_vec.x = x
    new_vec.y = y
    return new_vec

def compute_coordinates(bv1, bv2, v):
    det = (bv1.x * bv2.y) - (bv1.y * bv2.x)
    invbv1 = XY(bv2.y, -bv1.y)
    invbv2 = XY(-bv2.x, bv1.x)
    invbv1.multiply(1/det)
    invbv2.multiply(1/det)
    endvec = XY(invbv1.x * v.x + invbv2.x * v.y, invbv1.y * v.x + invbv2.y * v.y)
    return endvec

def is_at_right(v, p1, p2):
    p = XY(p2.x-p1.x, p2.y-p1.y)
    p = XY(p.y, -p.x)
    v1 = XY(v.x - p1.x, v.y - p1.y)
    return 0 < p.dot(v1) / (p.length() * v1.length())

#    a = p.y / p.x
#    b = p1.y - a * p1.x
#    return p.x/abs(p.x) * v.y < p.x/abs(p.x) * (a * v.x + b)    
#    if p.x < 0:
#        return v.y > a * v.x + b
#    else:
#        return v.y < a * v.x + b

print("Nowy wektor:")
v = Vector2D("v")
v.show()

print("Ustawmy kilka wspolrzednych:")
v.x = 1.0
v.y = 1.2
v.show()

print("Przeskalujemy?")
v.multiply(10)
v.show()
v.multiply(1/10)
v.show()
