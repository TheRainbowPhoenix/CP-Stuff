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
f.close()

# show_part(header)
show_part(spinner, 60)
