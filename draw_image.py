from PIL import Image, ImageDraw, ImageFont
import algs
from math import ceil, log2
import coords


class DrawTable:
    def __init__(self, units, mode='Вейч'):
        func = {'Карно': algs.get_karno, 'Вейч': algs.get_veych}
        self.matrix, self.su = func[mode](units)
        self.units = units

        self.font = ImageFont.truetype(r"fonts/Arial.ttf", size=45)

    def draw(self):
        count_of_args = ceil(log2(max(self.units) + 1))
        crd = coords.Coords(count_of_args)
        image = Image.new("RGBA", crd.size, (255, 255, 255, 255))
        draw = ImageDraw.Draw(image)
        for j in range(len(self.matrix)):
            for i in range(len(self.matrix[j])):
                draw.rectangle((crd.get_table_cell_coords(i, j),
                                crd.get_table_cell_coords(i + 1, j + 1)), outline='black')
                draw.text(crd.get_table_cell_coords(i, j),
                          text=str(int(self.matrix[j][i] in self.units)),
                          fill='black',
                          font=self.font)
        print(self.su)
        for j in range(len(self.su[0])):
            for i in range(count_of_args//2):
                if self.su[0][j][i*2] == '1':
                    draw.line((crd.get_left_arg(i, j), crd.get_left_arg(i, j+1)), fill='black')

        for j in range(len(self.su[1])):
            for i in range(count_of_args - count_of_args // 2):
                if self.su[1][j][i * 2] == '1':
                    draw.line((crd.get_top_arg(j, i), crd.get_top_arg(j+1, i)), fill='black')
        image.save('1.png')


a = DrawTable((1, 2, 16))
a.draw()

