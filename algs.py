import numpy as np
from math import ceil, log2


def get_veych_order(count_of_args):
    # count_of_args <= 27, else MemoryError
    """Returned matrix with placement order nums for Veych diagram"""
    matrix = np.array([[0]], int)
    for i in range(count_of_args):
        if i % 2 == 1:
            matrix = np.vstack((np.flip(matrix, 0) + 2 ** i, matrix))
        else:
            matrix = np.hstack((np.flip(matrix, 1) + 2 ** i, matrix))
    return matrix


def get_karno_order(count_of_args):
    # count_of_args <= 27, else MemoryError
    """Returned matrix with placement order nums for Karno cards"""
    matrix = np.array([[0]], int)
    for i in range(count_of_args):
        if i >= ceil(count_of_args / 2):
            matrix = np.vstack((matrix, np.flip(matrix, 0) + 2 ** i))
        else:
            matrix = np.hstack((matrix, np.flip(matrix, 1) + 2 ** i))
    return matrix


def to_bin(matrix):  # now that function is useless
    # matrix->count_of_args <= 17, else long time
    """Convert all nums in matrix to bin with same size"""
    maximum = len(np.binary_repr(np.max(matrix)))
    tbin = np.vectorize(lambda e: f'%0{maximum}i' % int(np.binary_repr(e)))
    mtbin = np.vectorize(lambda e: tbin(e))
    return mtbin(matrix)


def get_same_units(matrix):
    """Returned same units for every column/string of matrix(bitwise and of all elements)"""
    vertical = np.max(matrix)
    horizontal = np.max(matrix)
    for i in matrix:
        vertical = np.bitwise_and(i, vertical)
    for j in np.transpose(matrix):
        horizontal = np.bitwise_and(horizontal, j)

    def for_out(arr):
        return f'%0{len(np.binary_repr(np.max(arr)))}i'

    to_bin_hor = np.vectorize(lambda e: for_out(horizontal) % int(np.binary_repr(e)))
    to_bin_vert = np.vectorize(lambda e: for_out(vertical) % int(np.binary_repr(e)))
    return to_bin_hor(horizontal), to_bin_vert(vertical)


def get_table(matrix, units):

    su = get_same_units(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = int(matrix[i][j] in units)
    return matrix, su


def get_karno(units):
    matrix = get_karno_order(ceil(log2(max(units)+1)))
    return get_table(matrix, units)


def get_veych(units):
    matrix = get_veych_order(ceil(log2(max(units)+1)))
    return get_table(matrix, units)

