from mymatrix import determinant, inverse, matrix, self_test


def test_book_examples() -> None:
    self_test()


def test_inverse_does_not_require_third_party_packages() -> None:
    value = inverse(matrix([[2, 3], [1, 2]]))
    assert value.values == [[2.0, -3.0], [-1.0, 2.0]]
    assert determinant(matrix([[4]])) == 4
