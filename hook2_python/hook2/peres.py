import os
import sys

import pefile

from io import BytesIO


class PeRes():

    def __init__(self, file_name):
        self._filename = os.path.basename(file_name)

        try:
            self._pe = pefile.PE(file_name)
        except Exception as e:
            print(f"!!! FAILED \"{self._filename}\" : {e}")
            sys.exit(0)

    def get_resource_rom(self, save_extracted=False) -> bytes:
        if hasattr(self._pe, 'DIRECTORY_ENTRY_RESOURCE'):
            for resource_type in self._pe.DIRECTORY_ENTRY_RESOURCE.entries:
                if pefile.RESOURCE_TYPE.get(resource_type.struct.Id, '-') == 'RT_RCDATA':
                    if hasattr(resource_type, 'directory'):
                        for resource_id in resource_type.directory.entries:

                            if hasattr(resource_id, 'directory'):
                                for resource_item in resource_id.directory.entries:
                                    if resource_id.id == 3070:
                                        ROM_offset = resource_item.data.struct.OffsetToData
                                        ROM_size = resource_item.data.struct.Size

                                        data = self._pe.get_data(resource_item.data.struct.OffsetToData,
                                                                 resource_item.data.struct.Size)

                                        print(f"ROM @ {ROM_offset}:{ROM_size}")

                                        if save_extracted:
                                            with open(f"files/{resource_id.id}extract.bin", "wb+") as f:
                                                f.write(data)

                                        return data


if __name__ == '__main__':
    filename = "files/OSupdateDLL_original.dll"
    pe_res = PeRes(filename)
    pe_res.get_resource_rom(True)
