from PIL import Image
import numpy as np

def show_part(part, xdim=640):
    """
    Convert and show an image from a bytes part
    """
    MASK5 = 0b011111
    MASK6 = 0b111111

    im = np.frombuffer(part, dtype=np.uint16)
    b = (im & MASK5) << 3
    g = ((im >> 5) & MASK6) << 2
    r = ((im >> (5 + 6)) & MASK5) << 3

    rgb = np.dstack((r,g,b)).astype(np.uint8)


    mode = 'RGB'
    ydim = len(rgb[0]) // xdim

    image = Image.frombytes('RGB', (xdim, ydim), rgb, 'raw')
    image.show()



f = open("win/exe_parts/.rdata", "rb")

header = f.read(5396*2)
spinner = f.read(3360*2)

# data = f.read()

# show_part(header)
# show_part(spinner, 60)

pad = f.read(88 * 2)

button_system = f.read(159*16*4 *2)
# show_part(button_system, 159)

_ = f.read(160 * 2)

button_system_click = f.read(159*16*4 *2)
# show_part(button_system_click, 159)


_ = f.read(160 * 2)

button_com = f.read(159*16*4 *2)
# show_part(button_com, 159)

_ = f.read(160 * 2)

button_com_click = f.read(159*16*4 *2)
# show_part(button_com_click, 159)

_ = f.read(160 * 2)

button_prog = f.read(159*16*4 *2)
# show_part(button_prog, 159)

_ = f.read(160 * 2)

button_prog_click = f.read(159*16*4 *2)
# show_part(button_prog_click, 159)


_ = f.read(160 * 2)

button_fin = f.read(159*16*4 *2)
# show_part(button_fin, 159)

_ = f.read(160 * 2)

button_fin_click = f.read(159*16*4 *2)
# show_part(button_fin_click, 159)



_ = f.read(160 * 2)

button_seq = f.read(159*16*4 *2)
show_part(button_seq, 159)

_ = f.read(160 * 2)

button_seq_click = f.read(159*16*4 *2)
show_part(button_seq_click, 159)


# Close

f.close()