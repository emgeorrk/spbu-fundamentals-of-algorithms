import numpy as np
from numpy.typing import NDArray
from math import fabs


def lu(A: NDArray, permute: bool) -> tuple[NDArray, NDArray, NDArray]:
    if permute==False:
        n = len(A)
        L = np.zeros_like(A)
        U = A.copy()
        for i in range(n):
            for j in range(n):
                L[i][j] = 0.0

        for i in range(n):
            for j in range(i, n):
                L[j][i]=U[j][i]/U[i][i]

        for t in range(1, n):
            for i in range(t-1, n):
                for j in range(i, n):
                    L[j][i]=U[j][i]/U[i][i]

            for i in range(t, n):
                for j in range(t-1, n):
                    U[i][j]=U[i][j]-L[i][t-1]*U[t-1][j]
        return(L, U, np.eye(n))
    else:
        n = len(A)
        C = A
        P = np.zeros_like(A)
        for i in range(n): P[i][i] = 1.

        for i in range(n):
            pivotValue = 0.
            pivot = -1.
            for row in range(i, n):
                if fabs(C[row][i] > pivotValue):
                    pivotValue = fabs(C[row][i])
                    pivot = row
            if pivotValue != 0:
                P[pivot], P[i] = P[i], P[pivot]
                C[pivot], C[i] = C[i], C[pivot]
                for j in range(i+1, n):
                    C[j][i] /= C[i][i]
                    for k in range(i+1, n):
                        C[j][k] -= C[j][i]*C[i][k]
        print(C)
        L = np.zeros_like(A)
        U = np.zeros_like(A)
        for i in range(n):
            for j in range(n):
                if i < j: U[i][j] = C[i][j]
                if i < j: L[i][j] = C[i][j]
                if i == j:
                    L[i][j] = 1.
                    U[i][j] = C[i][j]
        return (L, U, P)


def solve(L: NDArray, U: NDArray, P: NDArray, b: NDArray) -> NDArray:
    Y = np.linalg.solve(L, P @ b)
    X = np.linalg.solve(U, Y)

    return X


def get_A_b(a_11: float, b_1: float) -> tuple[NDArray, NDArray]:
    A = np.array([[a_11, -7.0, 0.0], [-3.0, 6.0, 2.0], [5.0, -1.0, 5.0]])
    b = np.array([b_1, 12.0, -39.0])
    return A, b


def get_A_b(a_11: float, b_1: float) -> tuple[NDArray, NDArray]:
    A = np.array([[a_11, 1.0, -3.0], [6.0, 2.0, 5.0], [1.0, 4.0, -3.0]])
    b = np.array([b_1, 12.0, -39.0])
    return A, b


if __name__ == "__main__":
    # Let's implement the LU decomposition with and without pivoting
    # and check its stability depending on the matrix elements
    p = 14  # modify from 7 to 16 to check instability
    a_11 = 3 + 10 ** (-p)  # add/remove 10**(-p) to check instability
    b_1 = -16 + 10 ** (-p)  # add/remove 10**(-p) to check instability
    A, b = get_A_b(a_11, b_1)
    # With pivoting
    # L, U, P = lu(A, permute=True)
    # x = solve(L, U, P, b)
    # assert np.all(np.isclose(x, [1, -7, 4])), f"The anwser {x} is not accurate enough"
    # Without pivoting
    L, U, P = lu(A, permute=False)
    x_ = solve(L, U, P, b)
    assert np.all(np.isclose(x_, [1, -7, 4])), f"The anwser {x_} is not accurate enough"