from .compress import Compress

class Patcher:
    pass
    def __init__(self):
        self._mods = []

    def load_mod(self):
        mod_lines = ""

        with open("mod.txt", 'r') as f:
            mod_lines = f.readlines()

        if len(mod_lines) < 1:
            print("Missing mod headers, exiting.")
            return

        header = mod_lines[0].strip()

        if not header.startswith("'ver"):
            print("Invalid mod headers, exiting.")
            return

        rom_version = header[4:]

        print(f"Targeting rom version {rom_version}")

        print(mod_lines)


    def load_compressed_rom(self, fileref):
            head = b'\x1F\x8B\x08\x00\x00\x00\x00\x00\x04\x00'
            rom_bootloader = fileref.read(0x2FF6)

            file = head + rom_bootloader

            # Compressed ROM at index 0x3000 has 9B byte missing, which is hardcoded in the ROM flasher.
            file += b'\x9b'

            file += fileref.read()

            # with open('files/out.gz', 'wb+') as out:
            #     out.write(file)

            data = Compress.inflate(file)

            with open("files/3070_orig.bin", "wb+") as out:
                out.write(data)




if __name__ == '__main__':
    patcher = Patcher()
    patcher.load_mod()

    with open("files/3070extract.bin", 'rb') as f:
        patcher.load_compressed_rom(f)