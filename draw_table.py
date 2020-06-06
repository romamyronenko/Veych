from PIL import Image, ImageDraw, ImageFont
import numpy as np
import algs


def crop_array(array, elem):
    '''Return array without rows and columns where all elements is elem.'''
    array = np.delete(array, np.where(np.all(np.all(array == elem, axis=2), axis=1)), axis=0)
    array = np.delete(array, np.where(np.all(np.all(array == elem, axis=2), axis=0)), axis=1)
    return array


def crop_image(text, font, bg, color):
    '''Return crop image.'''
    image = Image.new('RGBA', font.getsize(text), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text=text, fill=color, font=font)
    return Image.fromarray(crop_array(np.array(image), bg))


matrix, su = algs.get_veych((1,2,3, 4, 129), (11,))

background_arr = np.array([255, 255, 255, 0])

# fields
cell_padding = 10
arg_padding = 5
font_size = 60
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
cell_size = one.size[1] + cell_padding
arg_size = crop_image('1', small_font, background_arr, 'black').size[1] + arg_padding


table_shift = (image_padding + table_margin + len(str(su[0][0]))*arg_size,
               image_padding + table_margin + len(str(su[1][0]))*arg_size)
print(su)
print(arg_size, cell_size)
table_size = (su[1].size*cell_size, su[0].size*cell_size)
img_size = (table_shift[0] + table_size[0] + image_padding,
            table_shift[1] + table_size[1] + image_padding)

# ...


font = ImageFont.truetype(r'fonts/Arial.ttf', size=45)

one = crop_image('1', font, background_arr, 'black')
one.save('one.png')


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
for i in range(su[1].size):
    for j in range(len(su[1][0])):
        if su[1][i][j] == '1':
            draw.line(((table_shift[0] + (i)*cell_size,
                        image_padding + (j+1)*arg_size),
                       (table_shift[0] + (i+1)*cell_size,
                        image_padding + (j+1)*arg_size)), fill='black')
                        
for i in range(su[0].size):
    for j in range(len(su[0][0])):
        if su[0][i][j] == '1':
            draw.line(((image_padding + (j+1)*arg_size,
                        table_shift[1] + (i)*cell_size),
                       (image_padding + (j+1)*arg_size,
                        table_shift[1] + (i+1)*cell_size)), fill='black')
            
#image.alpha_composite(one, (0, 0))
image.save('1.png')

