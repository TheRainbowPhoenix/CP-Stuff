from PIL import Image
import numpy as np

import json


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


def show_part(part, xdim=640):
    """
    Convert and show an image from a bytes part
    """
    image = from_part(part, xdim)
    image.show()


def save_part(part, name, xdim=640):
    image = from_part(part, xdim)
    image.save(f"rdata/{name}.png", "PNG")


with open('assets-map.json') as assets_map_file:
    ASSETS = json.load(assets_map_file)

f = open("win/exe_parts/.rdata", "rb")

assets_map = {}

if True:
    for asset in ASSETS:
        payload = f.read(asset['size'] * 2)
        if 'name' in asset and asset["export"]:
            assets_map[asset['name']] = payload
            save_part(payload, asset['name'], asset['width'])

print("todo : more")

print("break me !")

"""
header = f.read(5396 * 2)
spinner = f.read(3360 * 2)

# data = f.read()

# show_part(header)
# show_part(spinner, 60)

pad = f.read(88 * 2)

def stop_read():
    buffer = bytearray()

    while True:
        try:
            buf = f.read(2)
        except:
            break
        buffer += buf

        if buf == b'\x00\x00':
            break

    return buffer


buttons = f.read(159 * 16 * 4 * 14 * 2)
show_part(buttons, 159)

for asset in ASSETS:
    if "name" in asset and asset["export"]:
        part = stop_read()
        save_part(part, asset['name'], asset['width'])

# buttons = f.read(159 * 16 * 4 * 14 * 2)
# show_part(buttons, 159)
" ""
button_system = f.read(159*16*4 *2)
save_part(button_system, "button_system", 159)

_ = f.read(160 * 2)

button_system_click = f.read(159*16*4 *2)
save_part(button_system_click, "button_system_click", 159)

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

"""
