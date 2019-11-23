import numpy as np
from math import ceil
from PIL import Image, ImageDraw, ImageFont
import os
import configparser
from math import log2, ceil


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


def to_bin(matrix):  # now that's function useless
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

    for_out = lambda arr: f'%0{len(np.binary_repr(np.max(arr)))}i'
    to_bin_hor = np.vectorize(lambda e: for_out(horizontal) % int(np.binary_repr(e)))
    to_bin_vert = np.vectorize(lambda e: for_out(vertical) % int(np.binary_repr(e)))
    return to_bin_vert(vertical), to_bin_hor(horizontal)


def config():
    if os.path.isfile('config'):
        print('ok')
        image_config = dict()
    else:
        image_config = {
            'image_pd': 5,
            'font_size': 15,
            'arg_font_size': 10,
            'pd': 3,
            'arg_pd': 3,
            'table_margin': 3,
            'arg_margin': 3
        }
    return image_config


def draw_image(units):
    pass


class DrawImage:
    image_config = {
        'image_pd': 5,
        'cell_lr_pd': 5,
        'cell_tb_pd': 5,
        'table_left_pd': 3,
        'table_top_pd': 3,
        'arg_lr_pd': 2,
        'arg_tb_pd': 2,

    }
    font = ImageFont.truetype(r'C:\WINDOWS\Fonts\Arial.ttf', 40)
    arg_font = ImageFont.truetype(r'C:\WINDOWS\Fonts\Arial.ttf', 35)

    def __init__(self, units):
        self.units = units
        self.count_of_args = ceil(log2(max(self.units) + 1))
        self.count_of_hor_args = self.count_of_args//2
        self.count_of_vert_args = self.count_of_args - self.count_of_hor_args
        print(self.count_of_vert_args, self.count_of_hor_args)
        self.matrix, self.args = self.found_matrix()

        # table
        self.text_size = self.font.getsize("0")
        self.cell_size = (self.text_size[0] + self.image_config['cell_lr_pd']*2,
                          self.text_size[1] + self.image_config['cell_tb_pd']*2)
        self.table_size = (self.cell_size[0]*2**self.count_of_vert_args,
                           self.cell_size[1]*2**self.count_of_hor_args)

        # args
        self.arg_text_size = self.arg_font.getsize(f'X{max(self.units)}')
        self.arg_cell_size = (self.arg_text_size[0] + self.image_config['arg_lr_pd']*2,
                              self.arg_text_size[1] + self.image_config['arg_tb_pd']*2)
        self.args_size = (self.arg_cell_size[0]*self.count_of_hor_args + self.image_config['table_left_pd']
                          + self.image_config['image_pd'],
                          self.arg_cell_size[1]*self.count_of_vert_args + self.image_config['table_top_pd']
                          + self.image_config['image_pd'])

        # image
        self.image_size = (self.image_config['image_pd']*2 + self.table_size[0] + self.args_size[0],
                           self.image_config['image_pd']*2 + self.table_size[1] + self.args_size[1])

        # draw
        self.image = Image.new("RGBA", self.image_size, (1000, 1000, 1000, 1000))
        self.draw = ImageDraw.Draw(self.image)
        self.draw_table()
        print(self.args)
        print(self.matrix)

        self.image.save('1.png')
        self.image.close()

    def draw_table(self):
        for i in range(2**self.count_of_hor_args+1):
            self.draw.line(((self.args_size[0],
                             self.args_size[1] + self.cell_size[1] * i),
                            (self.args_size[0] + self.table_size[0],
                             self.args_size[1] + self.cell_size[1] * i)), fill='black')

        for i in range(2**self.count_of_vert_args+1):
            self.draw.line(((self.args_size[0] + self.cell_size[0] * i,
                             self.args_size[1]),
                            (self.args_size[0] + self.cell_size[0] * i,
                             self.args_size[1] + self.table_size[1])), fill='black')
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                size = self.arg_font.getsize(str(self.matrix[i][j]))
                self.draw.text((self.args_size[0] + self.cell_size[0] * j + (self.cell_size[0] - size[0])/2,
                                self.args_size[1] + self.cell_size[1] * i ),
                               text=str(self.matrix[i][j]), font=self.font, fill='black')

    def found_matrix(self):
        """Returned matrix with placed 0 and 1"""
        order = get_veych_order(self.count_of_args)
        args = get_same_units(order)
        matrix = [[1 if j in self.units else 0 for j in i]for i in order]
        return matrix, args

    def get_count_of_args(self):
        """Returned count of arguments"""
        return self.count_of_args


a = DrawImage((1, 2, 40))
# a.draw()
# print(a.get_width(), a.get_height())
