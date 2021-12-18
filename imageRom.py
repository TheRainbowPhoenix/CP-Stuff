from PIL import Image
import numpy as np
f = open("lib/VERSIONS\\02.00.1000.0000\\3070.bin", "rb")
l = f.read()
f.close()

MASK5 = 0b011111
MASK6 = 0b111111

# while len(l)%32 != 0:
#     l += b'\x00'


dt = np.dtype(np.uint16)
dt = dt.newbyteorder('>')
# np.frombuffer(buf, dtype=dt)

im = np.frombuffer(l, dtype=dt)

# im = (im << 8) | (im & 0xff)

r = (im >> 8) & 0b011111000
g = (im >> 3) & 0b011111100
b = (im << 3) & 0b011111000

# b = (im & MASK5) << 3
# g = ((im >> 5) & MASK6) << 2
# r = ((im >> (5 + 6)) & MASK5) << 3

rgb = np.dstack((r,g,b)).astype(np.uint8)


mode = 'RGB'
xdim = 640
ydim = len(rgb[0]) // xdim

image = Image.frombytes('RGB', (xdim, ydim), rgb, 'raw')
image.show()