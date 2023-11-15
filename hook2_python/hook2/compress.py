import zlib


class Compress:
    CHUNK = 0x40000  # 256k Chunks
    LEVEL = 6  # Compression level 6
    MEM_LEVEL = 9  # Zlib, 1 - 9, 9 is best, fast and more compact.

    @classmethod
    def deflate(cls, data):
        compress = zlib.compressobj(
            cls.LEVEL,  # level: 0-9
            zlib.DEFLATED,  # method: must be DEFLATED
            -zlib.MAX_WBITS,  # window size in bits:
            #   -15..-8: negate, suppress header
            #   8..15: normal
            #   16..30: subtract 16, gzip header
            cls.MEM_LEVEL,  # mem level: 1..8/9
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

    @classmethod
    def inflate(cls, data):
        # decompress = zlib.decompressobj(
        #         zlib.MAX_WBITS | 16  # see above
        # )
        inflated = zlib.decompress(data, zlib.MAX_WBITS | 16)
        # inflated += decompress.flush()
        return inflated
