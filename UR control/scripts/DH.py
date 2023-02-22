import math as m
import numpy as np
np.set_printoptions(suppress = True)

DH = [[0, 0, 0.15185, 1/2*m.pi], [0, -0.24355, 0, 0], [0, -0.2132, 0, 0], [0, 0, 0.13105, 1/2*m.pi], [0, 0, 0.08535, -1/2*m.pi], [0, 0, 0.0921, 0], [0,0, 0.1, 0]]

T = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(len(DH))]

for i in range(len(DH)):
    T[i][0][0] = m.cos(DH[i][0]); T[i][0][1] = -m.sin(DH[i][0]) * m.cos(DH[i][3]); T[i][0][2] = m.sin(DH[i][0]) * m.sin(DH[i][3]); T[i][0][3] = DH[i][1] * m.cos(DH[i][0])

    T[i][1][0] = m.sin(DH[i][0]); T[i][1][1] = m.cos(DH[i][0] * m.cos(DH[i][3])); T[i][1][2] = -m.cos(DH[i][0]) * m.sin(DH[i][3]); T[i][1][3] = DH[i][1] * m.sin(DH[i][0])

    T[i][2][0] = 0; T[i][2][1] = m.sin(DH[i][3]); T[i][2][2] = m.cos(DH[i][3]); T[i][2][3] = DH[i][2]

    T[i][3][0] = 0; T[i][3][1] = 0; T[i][3][2] = 0; T[i][3][3] = 1

arr = np.array(T)
# print(arr)


vec = [[0 for _ in range(4)] for _ in range(4)]
vec[2][2] = 1/2*m.pi; vec[3][3] = 1
arr2 = np.array(vec)

print(np.matmul(arr[6], arr2))



