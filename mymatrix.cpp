// Elementary matrix algorithms from "Programmer's Mathematics 3".
// Indices are deliberately one-based to correspond to the book and Ruby source.
#include <algorithm>
#include <cassert>
#include <cmath>
#include <iostream>
#include <stdexcept>
#include <utility>
#include <vector>

using Number = double;

struct Vector {
  std::vector<Number> data;
  explicit Vector(int n = 0) : data(n) {}
  Vector(std::initializer_list<Number> values) : data(values) {}
  int dim() const { return static_cast<int>(data.size()); }
  Number& operator[](int i) { return data.at(i - 1); }
  Number operator[](int i) const { return data.at(i - 1); }
};

struct Matrix {
  std::vector<std::vector<Number>> data;
  Matrix(int rows, int cols) : data(rows, std::vector<Number>(cols)) {}
  Matrix(std::initializer_list<std::initializer_list<Number>> values) {
    for (const auto& row : values) data.emplace_back(row);
    if (data.empty() || data.front().empty()) throw std::invalid_argument("matrix is empty");
    for (const auto& row : data)
      if (row.size() != data.front().size()) throw std::invalid_argument("matrix is not rectangular");
  }
  int rows() const { return static_cast<int>(data.size()); }
  int cols() const { return static_cast<int>(data.front().size()); }
  Number& operator()(int i, int j) { return data.at(i - 1).at(j - 1); }
  Number operator()(int i, int j) const { return data.at(i - 1).at(j - 1); }
};

void vector_add(Vector& a, const Vector& b) {
  if (a.dim() != b.dim()) throw std::invalid_argument("vector size mismatch");
  for (int i = 1; i <= a.dim(); ++i) a[i] += b[i];
}
void vector_times(Vector& vector, Number scalar) {
  for (int i = 1; i <= vector.dim(); ++i) vector[i] *= scalar;
}
void matrix_add(Matrix& a, const Matrix& b) {
  if (a.rows() != b.rows() || a.cols() != b.cols()) throw std::invalid_argument("matrix size mismatch");
  for (int i = 1; i <= a.rows(); ++i)
    for (int j = 1; j <= a.cols(); ++j) a(i, j) += b(i, j);
}
void matrix_times(Matrix& a, Number scalar) {
  for (int i = 1; i <= a.rows(); ++i)
    for (int j = 1; j <= a.cols(); ++j) a(i, j) *= scalar;
}
void matrix_vector_prod(const Matrix& a, const Vector& v, Vector& result) {
  if (a.cols() != v.dim() || a.rows() != result.dim()) throw std::invalid_argument("size mismatch");
  for (int i = 1; i <= a.rows(); ++i) {
    result[i] = 0;
    for (int k = 1; k <= a.cols(); ++k) result[i] += a(i, k) * v[k];
  }
}
void matrix_prod(const Matrix& a, const Matrix& b, Matrix& result) {
  if (a.cols() != b.rows() || result.rows() != a.rows() || result.cols() != b.cols())
    throw std::invalid_argument("size mismatch");
  for (int i = 1; i <= a.rows(); ++i)
    for (int j = 1; j <= b.cols(); ++j) {
      result(i, j) = 0;
      for (int k = 1; k <= a.cols(); ++k) result(i, j) += a(i, k) * b(k, j);
    }
}

Matrix operator+(Matrix a, const Matrix& b) { matrix_add(a, b); return a; }
Matrix operator-(Matrix a) { matrix_times(a, -1); return a; }
Matrix operator-(Matrix a, const Matrix& b) { return a + -Matrix(b); }
Matrix operator*(Matrix a, Number s) { matrix_times(a, s); return a; }
Matrix operator*(Number s, Matrix a) { return a * s; }
Vector operator*(Vector a, Number s) { vector_times(a, s); return a; }
Vector operator*(Number s, Vector a) { return a * s; }
Vector operator*(const Matrix& a, const Vector& v) { Vector result(a.rows()); matrix_vector_prod(a, v, result); return result; }
Matrix operator*(const Matrix& a, const Matrix& b) { Matrix result(a.rows(), b.cols()); matrix_prod(a, b, result); return result; }

void lu_decomp(Matrix& matrix) {
  for (int k = 1; k <= std::min(matrix.rows(), matrix.cols()); ++k) {
    if (matrix(k, k) == 0) throw std::domain_error("zero pivot; use PLU decomposition");
    for (int i = k + 1; i <= matrix.rows(); ++i) matrix(i, k) /= matrix(k, k);
    for (int i = k + 1; i <= matrix.rows(); ++i)
      for (int j = k + 1; j <= matrix.cols(); ++j) matrix(i, j) -= matrix(i, k) * matrix(k, j);
  }
}
std::pair<Matrix, Matrix> lu_split(const Matrix& lu) {
  int size = std::min(lu.rows(), lu.cols());
  Matrix lower(lu.rows(), size), upper(size, lu.cols());
  for (int i = 1; i <= lu.rows(); ++i)
    for (int j = 1; j <= size; ++j) lower(i, j) = i > j ? lu(i, j) : (i == j ? 1 : 0);
  for (int i = 1; i <= size; ++i)
    for (int j = 1; j <= lu.cols(); ++j) upper(i, j) = i > j ? 0 : lu(i, j);
  return {lower, upper};
}
Number determinant(Matrix matrix) {
  if (matrix.rows() != matrix.cols()) throw std::invalid_argument("matrix is not square");
  lu_decomp(matrix);
  Number result = 1;
  for (int i = 1; i <= matrix.rows(); ++i) result *= matrix(i, i);
  return result;
}
void solve_lu(const Matrix& lu, Vector& y) {
  if (lu.rows() != lu.cols() || lu.rows() != y.dim()) throw std::invalid_argument("size mismatch");
  for (int i = 1; i <= y.dim(); ++i)
    for (int j = 1; j < i; ++j) y[i] -= lu(i, j) * y[j];
  for (int i = y.dim(); i >= 1; --i) {
    for (int j = i + 1; j <= y.dim(); ++j) y[i] -= lu(i, j) * y[j];
    y[i] /= lu(i, i);
  }
}
void solve(Matrix& a, Vector& y) { lu_decomp(a); solve_lu(a, y); }
Matrix inverse(Matrix matrix) {
  if (matrix.rows() != matrix.cols()) throw std::invalid_argument("matrix is not square");
  lu_decomp(matrix);
  Matrix result(matrix.rows(), matrix.cols());
  for (int col = 1; col <= result.cols(); ++col) {
    Vector rhs(result.rows()); rhs[col] = 1;
    solve_lu(matrix, rhs);
    for (int row = 1; row <= result.rows(); ++row) result(row, col) = rhs[row];
  }
  return result;
}
// The returned table identifies the source row now used at each row position.
Vector plu_decomp(Matrix& matrix) {
  Vector pivot(matrix.rows());
  for (int i = 1; i <= pivot.dim(); ++i) pivot[i] = i;
  for (int k = 1; k <= std::min(matrix.rows(), matrix.cols()); ++k) {
    int winner = k;
    for (int i = k + 1; i <= matrix.rows(); ++i)
      if (std::abs(matrix(static_cast<int>(pivot[i]), k)) > std::abs(matrix(static_cast<int>(pivot[winner]), k))) winner = i;
    std::swap(pivot[k], pivot[winner]);
    if (matrix(static_cast<int>(pivot[k]), k) == 0) throw std::domain_error("singular matrix");
    for (int i = k + 1; i <= matrix.rows(); ++i) matrix(static_cast<int>(pivot[i]), k) /= matrix(static_cast<int>(pivot[k]), k);
    for (int i = k + 1; i <= matrix.rows(); ++i)
      for (int j = k + 1; j <= matrix.cols(); ++j)
        matrix(static_cast<int>(pivot[i]), j) -= matrix(static_cast<int>(pivot[i]), k) * matrix(static_cast<int>(pivot[k]), j);
  }
  return pivot;
}

bool close(Number left, Number right) { return std::abs(left - right) < 1e-9; }
void tests() {
  Matrix a{{3, 1}, {4, 1}}, b{{10, 20}, {30, 40}};
  Matrix product = a * b;
  assert(product(1, 1) == 60 && product(2, 2) == 120);
  Vector vector{1, 2};
  Vector mv = a * vector;
  assert(mv[1] == 5 && mv[2] == 6);
  assert(close(determinant(Matrix{{2, 1, 3, 2}, {6, 6, 10, 7}, {2, 7, 6, 6}, {4, 5, 10, 9}}), -12));
  Matrix equations{{2, 3, 3}, {3, 4, 2}, {-2, -2, 3}};
  Vector rhs{9, 9, 2}; solve(equations, rhs);
  assert(close(rhs[1], 3) && close(rhs[2], -1) && close(rhs[3], 2));
  Matrix inv = inverse(Matrix{{2, 3}, {1, 2}});
  assert(close(inv(1, 1), 2) && close(inv(1, 2), -3) && close(inv(2, 1), -1) && close(inv(2, 2), 2));
  std::cout << "all tests passed\n";
}
int main() { tests(); }
