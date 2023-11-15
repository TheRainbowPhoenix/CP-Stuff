from PIL import Image

from .font import small_map

# Length : 52 char

img = Image.new('RGB', (320, 528))
# img.putpixel((30,60), (155,155,55))
# img.save('sqr.png')

px = 0
py = 0

w = (255, 255, 255)


def putChar(c):
    if c == '0':
        pm = small_map["0"]
        x = 0
        y = 0
        mx = pm["size"][0]
        my = pm["size"][1]

        for p in pm["data"]:
            if x >= mx:
                y += 1
                x = 0
            else:
                x += 1

            if p == 1:
                img.putpixel(px + x, py + y, w)



def putStr(text):
    for c in text:
        putChar(c)

if __name__ == '__main__':
    putStr("0123456789abcdefghikklmnopqrstuvwxyz")
    img.show()
