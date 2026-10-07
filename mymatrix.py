#!/usr/bin/env python3
"""Elementary matrix algorithms from *Programmer's Mathematics 3*.

The module deliberately uses small, explicit loops so the calculation steps are
easy to follow.  Vector and Matrix indices are one-based, matching the book.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


class MatrixError(ValueError):
    """Raised when an operation is not defined for the supplied dimensions."""


@dataclass
class MyVector:
    values: list[float]

    def __init__(self, size_or_values: int | Iterable[float]):
        self.values = ([0.0] * size_or_values if isinstance(size_or_values, int)
                       else list(size_or_values))

    def __getitem__(self, index: int) -> float:
        return self.values[index - 1]

    def __setitem__(self, index: int, value: float) -> None:
        self.values[index - 1] = value

    def dim(self) -> int:
        return len(self.values)

    def copy(self) -> "MyVector":
        return MyVector(self.values)

    def __add__(self, other: "MyVector") -> "MyVector":
        result = self.copy()
        vector_add(result, other)
        return result

    def __neg__(self) -> "MyVector":
        return self * -1

    def __sub__(self, other: "MyVector") -> "MyVector":
        return self + -other

    def __mul__(self, value: float) -> "MyVector | float":
        if isinstance(value, (int, float)):
            result = self.copy()
            vector_times(result, value)
            return result
        raise TypeError("vectors can only be multiplied by scalars")

    __rmul__ = __mul__


@dataclass
class MyMatrix:
    values: list[list[float]]

    def __init__(self, rows_or_values: int | Sequence[Sequence[float]], cols: int | None = None):
        if isinstance(rows_or_values, int):
            if cols is None:
                raise TypeError("number of columns is required")
            self.values = [[0.0] * cols for _ in range(rows_or_values)]
        else:
            self.values = [list(row) for row in rows_or_values]
            if not self.values or not self.values[0] or any(len(row) != len(self.values[0]) for row in self.values):
                raise MatrixError("a matrix must be a non-empty rectangle")

    def __getitem__(self, key: tuple[int, int]) -> float:
        row, col = key
        return self.values[row - 1][col - 1]

    def __setitem__(self, key: tuple[int, int], value: float) -> None:
        row, col = key
        self.values[row - 1][col - 1] = value

    def dim(self) -> tuple[int, int]:
        return len(self.values), len(self.values[0])

    def copy(self) -> "MyMatrix":
        return MyMatrix(self.values)

    def __add__(self, other: "MyMatrix") -> "MyMatrix":
        result = self.copy()
        matrix_add(result, other)
        return result

    def __neg__(self) -> "MyMatrix":
        return self * -1

    def __sub__(self, other: "MyMatrix") -> "MyMatrix":
        return self + -other

    def __mul__(self, other: float | MyVector | "MyMatrix") -> "MyMatrix | MyVector | float":
        rows, cols = self.dim()
        if isinstance(other, (int, float)):
            result = self.copy()
            matrix_times(result, other)
            return result
        if isinstance(other, MyVector):
            if cols != other.dim():
                raise MatrixError("size mismatch")
            result = MyVector(rows)
            matrix_vector_prod(self, other, result)
            return result
        if isinstance(other, MyMatrix):
            if cols != other.dim()[0]:
                raise MatrixError("size mismatch")
            result = MyMatrix(rows, other.dim()[1])
            matrix_prod(self, other, result)
            return result
        raise TypeError("unsupported matrix product")

    __rmul__ = __mul__


def vector(elements: Iterable[float]) -> MyVector:
    return MyVector(elements)


def matrix(elements: Sequence[Sequence[float]]) -> MyMatrix:
    return MyMatrix(elements)


def vector_add(a: MyVector, b: MyVector) -> None:
    if a.dim() != b.dim():
        raise MatrixError("size mismatch")
    for i in range(1, a.dim() + 1):
        a[i] += b[i]


def vector_times(vec: MyVector, number: float) -> None:
    for i in range(1, vec.dim() + 1):
        vec[i] *= number


def matrix_add(a: MyMatrix, b: MyMatrix) -> None:
    if a.dim() != b.dim():
        raise MatrixError("size mismatch")
    rows, cols = a.dim()
    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            a[i, j] += b[i, j]


def matrix_times(mat: MyMatrix, number: float) -> None:
    rows, cols = mat.dim()
    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            mat[i, j] *= number


def matrix_vector_prod(a: MyMatrix, v: MyVector, result: MyVector) -> None:
    rows, cols = a.dim()
    if cols != v.dim() or rows != result.dim():
        raise MatrixError("size mismatch")
    for i in range(1, rows + 1):
        result[i] = sum(a[i, k] * v[k] for k in range(1, cols + 1))


def matrix_prod(a: MyMatrix, b: MyMatrix, result: MyMatrix) -> None:
    a_rows, a_cols = a.dim()
    b_rows, b_cols = b.dim()
    if (a_cols, b_cols) != result.dim() or a_cols != b_rows:
        raise MatrixError("size mismatch")
    for i in range(1, a_rows + 1):
        for j in range(1, b_cols + 1):
            result[i, j] = sum(a[i, k] * b[k, j] for k in range(1, a_cols + 1))


def lu_decomp(mat: MyMatrix) -> None:
    rows, cols = mat.dim()
    for k in range(1, min(rows, cols) + 1):
        if mat[k, k] == 0:
            raise MatrixError("zero pivot; use plu_decomp")
        for i in range(k + 1, rows + 1):
            mat[i, k] /= mat[k, k]
        for i in range(k + 1, rows + 1):
            for j in range(k + 1, cols + 1):
                mat[i, j] -= mat[i, k] * mat[k, j]


def lu_split(lu: MyMatrix) -> tuple[MyMatrix, MyMatrix]:
    rows, cols = lu.dim()
    size = min(rows, cols)
    lower, upper = MyMatrix(rows, size), MyMatrix(size, cols)
    for i in range(1, rows + 1):
        for j in range(1, size + 1):
            lower[i, j] = lu[i, j] if i > j else (1.0 if i == j else 0.0)
    for i in range(1, size + 1):
        for j in range(1, cols + 1):
            upper[i, j] = 0.0 if i > j else lu[i, j]
    return lower, upper


def determinant(mat: MyMatrix) -> float:
    rows, cols = mat.dim()
    if rows != cols:
        raise MatrixError("not square")
    lu_decomp(mat)
    answer = 1.0
    for i in range(1, rows + 1):
        answer *= mat[i, i]
    return answer


def solve_lu(lu: MyMatrix, y: MyVector) -> None:
    n = y.dim()
    for i in range(1, n + 1):
        for j in range(1, i):
            y[i] -= lu[i, j] * y[j]
    for i in range(n, 0, -1):
        for j in range(i + 1, n + 1):
            y[i] -= lu[i, j] * y[j]
        y[i] /= lu[i, i]


def solve(a: MyMatrix, y: MyVector) -> None:
    lu_decomp(a)
    solve_lu(a, y)


def inverse(mat: MyMatrix) -> MyMatrix:
    rows, cols = mat.dim()
    if rows != cols:
        raise MatrixError("not square")
    lu_decomp(mat)
    answer = MyMatrix([[1.0 if i == j else 0.0 for j in range(rows)] for i in range(rows)])
    for col in range(1, rows + 1):
        rhs = vector(answer[i, col] for i in range(1, rows + 1))
        solve_lu(mat, rhs)
        for row in range(1, rows + 1):
            answer[row, col] = rhs[row]
    return answer


def plu_decomp(mat: MyMatrix) -> MyVector:
    rows, cols = mat.dim()
    pivot = vector(range(1, rows + 1))
    for k in range(1, min(rows, cols) + 1):
        winner = max(range(k, rows + 1), key=lambda i: abs(mat[pivot[i], k]))
        pivot[k], pivot[winner] = pivot[winner], pivot[k]
        if mat[pivot[k], k] == 0:
            raise MatrixError("singular matrix")
        for i in range(k + 1, rows + 1):
            mat[pivot[i], k] /= mat[pivot[k], k]
        for i in range(k + 1, rows + 1):
            for j in range(k + 1, cols + 1):
                mat[pivot[i], j] -= mat[pivot[i], k] * mat[pivot[k], j]
    return pivot


def _close(a: float, b: float) -> bool:
    return abs(a - b) < 1e-9


def self_test() -> None:
    a = matrix([[3, 1], [4, 1]])
    b = matrix([[10, 20], [30, 40]])
    product = a * b
    assert product.values == [[60, 100], [70, 120]]
    assert (a * vector([1, 2])).values == [5, 6]
    assert _close(determinant(matrix([[2, 1, 3, 2], [6, 6, 10, 7], [2, 7, 6, 6], [4, 5, 10, 9]])), -12)
    source = matrix([[2, 3, 3], [3, 4, 2], [-2, -2, 3]])
    rhs = vector([9, 9, 2])
    solve(source, rhs)
    assert all(_close(x, y) for x, y in zip(rhs.values, [3, -1, 2]))
    inv = inverse(matrix([[2, 3], [1, 2]]))
    assert all(_close(x, y) for x, y in zip(inv.values[0] + inv.values[1], [2, -3, -1, 2]))
    print("all tests passed")


if __name__ == "__main__":
    self_test()
