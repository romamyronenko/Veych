from PIL import Image, ImageDraw, ImageFont
import numpy as np
import algs
from math import ceil, log2




def crop_array(array, elem):
    '''Return array without rows and columns where all elements is elem.'''
    array = np.delete(array, np.where(np.all(np.all(array == elem, axis=2), axis=1)), axis=0)
    array = np.delete(array, np.where(np.all(np.all(array == elem, axis=2), axis=0)), axis=1)
    return array


def crop_image(text, font, bg, color):
    '''Return crop image.'''
    image = Image.new('RGBA', font.getsize(text), (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text=text, fill=color, font=font)
    return Image.fromarray(crop_array(np.array(image), bg))


units = (1,2,3, 4, 256)
matrix, su = algs.get_veych(units, (11,))
count_of_args = ceil(log2(max(units)+1))
coa_left = count_of_args//2
coa_top = count_of_args - coa_left

background_arr = np.array([255, 255, 255, 255])

# fields
cell_padding = 10
arg_padding = 10
font_size = 45
small_font_size = 30
table_margin = 5
image_padding = 5

# fonts
font = ImageFont.truetype(r'fonts/Arial.ttf', size=font_size)
small_font = ImageFont.truetype(r'fonts/Arial.ttf', size=small_font_size)

one = crop_image('1', font, background_arr, 'black')
zero = crop_image('0', font, background_arr, 'black')
dash = crop_image('-', font, background_arr, 'black')

# other size
cell_size = one.size[1] + cell_padding*2
arg_size = crop_image('1', small_font, background_arr, 'black').size[1] + arg_padding*2


table_shift = (image_padding + table_margin + (coa_left)*arg_size,
               image_padding + table_margin + (coa_top)*arg_size)
print(su)
table_size = (su[1].size*cell_size, su[0].size*cell_size)
img_size = (table_shift[0] + table_size[0] + image_padding,
            table_shift[1] + table_size[1] + image_padding)

# ...


font = ImageFont.truetype(r'fonts/Arial.ttf', size=45)



background_arr = np.array([255, 255, 255, 255])
image = Image.new("RGBA", img_size, tuple(background_arr))
draw = ImageDraw.Draw(image)

# draw table
for i in range(su[0].size):
    for j in range(su[1].size):
        draw.rectangle(((table_shift[0] + cell_size*j, table_shift[1] + cell_size*i), 
                        (table_shift[0] + cell_size*(j + 1), table_shift[1] + cell_size*(i+1))), 
                        outline='black')
        if matrix[i][j] == 1:
            image.alpha_composite(one, (table_shift[0] + j*cell_size+(cell_size-one.size[0])//2, 
                                        table_shift[1] + i*cell_size+(cell_size-one.size[1])//2))
        elif matrix[i][j] == 2:
            image.alpha_composite(dash, (table_shift[0] + j*cell_size+(cell_size-dash.size[0])//2, 
                                         table_shift[1] + i*cell_size+(cell_size-dash.size[1])//2))
        else:
            image.alpha_composite(zero, (table_shift[0] + j*cell_size+(cell_size-zero.size[0])//2, 
                                         table_shift[1] + i*cell_size+(cell_size-zero.size[1])//2))
        
# draw args
"""
for i in range(su[1].size):
    for j in range(len(su[1][0])):
        if su[1][i][j] == '1':
            draw.line(((table_shift[0] + (i)*cell_size, image_padding + (j+1)*arg_size),
                       (table_shift[0] + (i+1)*cell_size, image_padding + (j+1)*arg_size)), 
                       fill='black')

for i in range(su[0].size):
    for j in range(len(su[0][0])):
        if su[0][i][j] == '1':
            draw.line(((image_padding + (j+1)*arg_size, table_shift[1] + (i)*cell_size),
                       (image_padding + (j+1)*arg_size, table_shift[1] + (i+1)*cell_size)), 
                       fill='black')
"""
x = table_shift[0]
x1 = table_shift[0]+2**(coa_top-1)*cell_size
y = image_padding + arg_size
draw.line((
           (x, y),
           (x1, y)
          ), fill='black')
text = crop_image(f'x{coa_top*2-1}', small_font, background_arr, 'black')
image.alpha_composite(text, (x+(x1-x-text.size[0])//2, y-arg_size+arg_padding))

for i in range(2, coa_top+1):
    for j in range(2**i):
        x = table_shift[0] + cell_size*2**(coa_top-i)*(1+4*j)
        x1 = table_shift[0] + cell_size*(2**(coa_top-i)*(2*(1+2*j)+1))
        y = image_padding + arg_size*i
        draw.line(((x, y), (x1, y)), fill='black')

        text = crop_image(f'x{(coa_top-i+1)*2-1}', small_font, background_arr, 'black')
        image.alpha_composite(text, (x+(x1-x-text.size[0])//2, y-arg_size+arg_padding))
        

x = image_padding + arg_size
y = table_shift[1]
y1 = table_shift[1]+2**(coa_left-1)*cell_size
draw.line((
           (x, y),
           (x, y1)
          ), fill='black')
text = crop_image(f'x{coa_left*2}', small_font, background_arr, 'black')
text = text.rotate(90, resample=Image.BICUBIC, expand=True)
image.alpha_composite(text, (x-arg_size+arg_padding, y+(y1-y-text.size[1])//2))

for i in range(2, coa_left+1):
    for j in range(2**i):
        y = table_shift[1] + cell_size*2**(coa_left-i)*(1+4*j)
        y1 = table_shift[1] + cell_size*(2**(coa_left-i)*(2*(1+2*j)+1))
        x = image_padding + arg_size*i
        draw.line(((x, y), (x, y1)), fill='black')
        
        text = crop_image(f'x{(coa_left-i+1)*2}', small_font, background_arr, 'black')
        text = text.rotate(90, resample=Image.BICUBIC, expand=True)
        image.alpha_composite(text, (x-arg_size+arg_padding, y+(y1-y-text.size[1])//2))
        


#image.alpha_composite(one, (0, 0))
image.save('1.png')

