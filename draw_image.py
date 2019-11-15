import numpy as np


def get_veych_order(count_of_args):
    # count_of_args <= 27, else error(MemoryError)
    """Returned matrix with placement order nums for Veych diagram"""
    matrix = np.array([[0]], int)
    for i in range(count_of_args):
        if i%2 == 1:
            matrix = np.vstack((np.flip(matrix, 0) + 2 ** i, matrix))
        else:
            matrix = np.hstack((np.flip(matrix, 1)+2**i, matrix))
    return matrix


def get_karno_order(count_of_args):
    # count_of_args <= 27, else error(MemoryError)
    """Returned matrix with placement order nums for Karno cards"""
    matrix = np.array([[0]], int)
    for i in range(count_of_args):
        if i//2%2 == 1:
            matrix = np.vstack((matrix, np.flip(matrix, 0) + 2 ** i))
        else:
            matrix = np.hstack((matrix, np.flip(matrix, 1)+2**i))
    return matrix


def to_bin(matrix):
    # matrix->count_of_args <= 17, else long time
    """Convert all nums in matrix to bin with same size"""
    maximum = len(np.binary_repr(np.max(matrix)))
    tbin = np.vectorize(lambda e: f'%0{maximum}i'%int(np.binary_repr(e)))
    mtbin = np.vectorize(lambda e: tbin(e))
    return mtbin(matrix)


print(get_veych_order(4))
print(to_bin(get_veych_order(4)))
# print(get_karno_order(4))

# x = to_bin(get_veych_order(3))
# with open('1.txt', 'w+') as f:
#     for i in x:
#         for j in i:
#             f.write(j)
#             f.write(' ')
#         f.write('\n')

# print(x)
