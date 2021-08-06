from PIL import Image
import numpy as np
f = open("win/exe_parts/.rdata", "rb")
l = f.read()
f.close()

MASK5 = 0b011111
MASK6 = 0b111111

im = np.frombuffer(l, dtype=np.uint16)
b = (im & MASK5) << 3
g = ((im >> 5) & MASK6) << 2
r = ((im >> (5 + 6)) & MASK5) << 3

rgb = np.dstack((r,g,b)).astype(np.uint8)


mode = 'RGB'
xdim = 640
ydim = len(rgb[0]) // xdim

image = Image.frombytes('RGB', (xdim, ydim), rgb, 'raw')
image.show()