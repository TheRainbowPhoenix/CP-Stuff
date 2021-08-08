import zlib

CHUNK = 0x40000  # 256k Chunks
LEVEL = 6  # Compression level 6
MEM_LEVEL = 9  # Zlib, 1 - 9, 9 is best, fast and more compact.


def deflate(data):
    compress = zlib.compressobj(
        LEVEL,  # level: 0-9
        zlib.DEFLATED,  # method: must be DEFLATED
        -zlib.MAX_WBITS,  # window size in bits:
        #   -15..-8: negate, suppress header
        #   8..15: normal
        #   16..30: subtract 16, gzip header
        MEM_LEVEL,  # mem level: 1..8/9
        0  # strategy:
        #   0 = Z_DEFAULT_STRATEGY
        #   1 = Z_FILTERED
        #   2 = Z_HUFFMAN_ONLY
        #   3 = Z_RLE
        #   4 = Z_FIXED
    )
    deflated = compress.compress(data)
    deflated += compress.flush()
    return deflated


"""
zlib.compressobj(...) ⇒ deflateInit(...)
compressobj.compress(...) ⇒ deflate(...)
zlib.decompressobj(...) ⇒ inflateInit(...)
decompressobj.decompress(...) ⇒ inflate(...)

"""


def inflate(data):
    # decompress = zlib.decompressobj(
    #         zlib.MAX_WBITS | 16  # see above
    # )
    inflated = zlib.decompress(data, zlib.MAX_WBITS | 16)
    # inflated += decompress.flush()
    return inflated


def process():
    head = b'\x1F\x8B\x08\x00\x00\x00\x00\x00\x04\x00'

    f = open("RCData3070.bin", "rb")
    l = f.read(0x2FF6)

    file = head + l

    file += b'\x9b'

    file += f.read()

    f.close()

    with open('out.gz', 'wb+') as out:
        out.write(file)

    data = inflate(file)

    with open('out.bin', 'wb+') as out:
        out.write(data)

    # Part 2

    f = open("RCData3069.bin", "rb")
    l = f.read(0x2FF6)

    file = head + l

    file += b'\x0B'

    file += f.read()

    f.close()

    with open('out-3069.gz', 'wb+') as out:
        out.write(file)

    data = inflate(file)

    with open('out-3069.bin', 'wb+') as out:
        out.write(data)

if __name__ == '__main__':
    process()
