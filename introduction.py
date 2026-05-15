from math import inf

#definicja jest w klasie Matrix w pliku matrix.py ale nie ma potrzeby go tu zamieszczac
def max_norm(self):
    return max([max([abs(x) for x in row]) for row in self._data])

def dot(v1, v2):
    if len(v1) != len(v2):
        return None
    result = 0
    for i in range(len(v1)):
        result += v1[i] * v2[i]
    return result

def maxi(vv):
    maxnum = -inf
    maxidx = -1
    for i in range(len(vv)):
        if vv[i] > maxnum:
            maxnum = vv[i]
            maxidx = i
    return maxidx

