from PIL import Image
import numpy as np
f0 = open("lib/VERSIONS\\02.01.1000.0000\\3070.bin", "rb")
l0 = bytearray(f0.read())
f0.close()

f1 = open("lib/VERSIONS\\02.01.2000.0000\\3070.bin", "rb")
l1 = bytearray(f1.read())
f1.close()

MASK5 = 0b011111
MASK6 = 0b111111

# while len(l)%32 != 0:
#     l += b'\x00'

len_l0 = len(l0)
len_l1 = len(l1)

ldiff = len_l0 - len_l1

if ldiff > 0:
    l1 += b'\x00' * ldiff
elif ldiff < 0:
    l0 += b'\x00' * abs(ldiff)

size = max(len_l1, len_l0)

# l = bytearray(size)
#
# for i in range(size):
#     l[i] = l0[i] ^ l1[i]

# l = bytes(a ^ b for a, b in zip(l1, l0))

dt = np.dtype(np.uint16)
dt = dt.newbyteorder('>')
# np.frombuffer(buf, dtype=dt)

im0 = np.frombuffer(l0, dtype=dt)
im1 = np.frombuffer(l1, dtype=dt)

im = np.bitwise_xor(im0, im1)

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