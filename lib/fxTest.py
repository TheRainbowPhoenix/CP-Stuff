import sys, ctypes, platform, os

"""
Call order :
- fxASPI_Init()
- fxASPI_GetDeviceNum(uint32_ptr=0) // dword ptr, 4 bytes
- fxASPI_WriteData(int=1, ptr=0x6, ptr_data?=0x30343018) // also -1 as 4th
    - fxASPI.29013D0
(If error)
- fxASPI_Term()

"""

if platform.system().lower() == 'windows':
    import os.path

    dll_name = "fxASPI.dll"
    enum_dll_name = "EnumDev.dll"

    current_path = os.path.abspath(os.path.dirname(__file__))

    dlldir_handle = None
    dll_path = os.path.dirname(os.path.abspath(__file__)) + os.path.sep

    os.environ['path'] = current_path + ';' + os.environ['path']
    sys.path.insert(0, current_path)
    if sys.version_info >= (3, 8):
        dlldir_handle = os.add_dll_directory(current_path)
    try:
        fx_aspi_lib = ctypes.windll.LoadLibrary(dll_name)
        fx_aspi_dll = ctypes.WinDLL(dll_name, winmode=0)

        enum_dev_lib = ctypes.windll.LoadLibrary(enum_dll_name)
        enum_dev_dll = ctypes.WinDLL(dll_name, winmode=0)

        init = fx_aspi_lib.fxASPI_Init()
        assert init == 1

        print(init)

        pv_enum_usb_a = getattr(enum_dev_lib, "_PVEnumUsbA@12")

        pv_devices = pv_enum_usb_a()


        #  fxASPI_GetDeviceNum (int32_t arg_4h);

        # fxASPI_WriteData (int32_t arg_4h, int32_t arg_28h, int32_t arg_20h);

        # 13889184
        # 15321604
        # arg = 15321604
        # device_num = fx_aspi_lib.fxASPI_GetDeviceNum(arg)
        # print(device_num)

        # fx_aspi_lib.fxASPI_Term() == 1


        # ecx = fxASPI_GetInquiry (int32_t arg_8h, int32_t arg_ch, int32_t arg_10h);


    finally:
        if dlldir_handle:
            dlldir_handle.close()

