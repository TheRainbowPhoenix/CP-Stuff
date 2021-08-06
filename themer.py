from PIL import Image
import numpy as np
import io


def from_part(part, xdim=640):
    """
    Convert and show an image from a bytes part
    """
    MASK5 = 0b011111
    MASK6 = 0b111111

    im = np.frombuffer(part, dtype=np.uint16)
    b = (im & MASK5) << 3
    g = ((im >> 5) & MASK6) << 2
    r = ((im >> (5 + 6)) & MASK5) << 3

    rgb = np.dstack((r, g, b)).astype(np.uint8)

    mode = 'RGB'
    ydim = len(rgb[0]) // xdim

    image = Image.frombytes('RGB', (xdim, ydim), rgb, 'raw')
    return image


def flatter(rbg):
    return (rbg[0] >> 3 << 11) + (rbg[1] >> 2 << 5) + (rbg[2] >> 3)

def to_part(image):
    """
    Convert RGB888 image to a 565

    pxl = 0b11111_111111_11111
           ' red 'green 'blue ' 
    """

    rgb = np.asarray(list(image.getdata()), dtype=np.uint16)

    rgb565 = np.array([flatter(pxl) for pxl in rgb], dtype=np.uint16)

    return rgb565.tobytes()


f = open("win/exe_parts/.rdata", "rb")

header = f.read(5396 * 2)
spinner = f.read(3360 * 2)

# data = f.read()
f.close()

img = from_part(spinner, 60)

out = to_part(img)

assert out == spinner
