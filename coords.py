fields = {
    'main': 5,

    'text_size': 15,
    'cell_size': 50,
    'table_field': 5,

    'arg_text_size': 10,
    'arg_cell_size': 50
}


class Coords:
    def __init__(self, count_of_args):
        self.count_of_args = count_of_args

    @property
    def args_size(self):
        left = (self.count_of_args//2)*fields['arg_cell_size']
        top = (self.count_of_args - self.count_of_args//2)*fields['arg_cell_size']
        return left, top

    @property
    def table_size(self):
        width = fields['cell_size']*2**(self.count_of_args - self.count_of_args//2)
        height = fields['cell_size']*2**(self.count_of_args//2)
        return width, height

    @property
    def size(self):
        width = fields['main']*2 + fields['table_field'] + self.args_size[0] + self.table_size[0] + 1
        height = fields['main']*2 + fields['table_field'] + self.args_size[1] + self.table_size[1] + 1
        return width, height

    def get_table_cell_coords(self, a, b):
        return (fields['main'] + self.args_size[0] + fields['table_field'] + fields['cell_size'] * a,
                fields['main'] + self.args_size[1] + fields['table_field'] + fields['cell_size'] * b)

    def get_left_arg(self, a, b):
        return (fields['main'] + fields['arg_cell_size'] * (a + 1),
                fields['main'] + fields['arg_cell_size'] * b + self.args_size[1] + fields['table_field'])

    def get_top_arg(self, a, b):
        return (fields['main'] + fields['arg_cell_size'] * a + self.args_size[0] + fields['table_field'],
                fields['main'] + fields['arg_cell_size'] * (b + 1))
