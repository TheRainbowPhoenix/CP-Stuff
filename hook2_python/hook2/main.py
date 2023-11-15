from .patcher import Patcher
from .peres import PeRes

from io import BytesIO


class Hook2:
    def __init__(self):
        self._patcher = Patcher()
        self._peres = None

    def load_init(self, os_update_dll_path: str):
        self._patcher.load_mod()

        self._peres = PeRes(os_update_dll_path)
        compressed_rom_data = self._peres.get_resource_rom()
        compressed_rom_file = BytesIO()
        compressed_rom_file.write(compressed_rom_data)

        self._patcher.load_compressed_rom(compressed_rom_file)


if __name__ == '__main__':
    hook2 = Hook2()
    hook2.load_init("files/OSupdateDLL_original.dll")
