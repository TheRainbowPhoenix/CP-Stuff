import sys, ctypes, platform, os

if platform.system().lower() == 'windows':
    import os.path

    dll_name = "OSupdateDLL.dll"

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

        init = fx_aspi_lib.OSUpdate("0", "0")
        assert init == 1

        print(init)

        # fx_aspi_lib.fxASPI_Term() == 1


        # ecx = fxASPI_GetInquiry (int32_t arg_8h, int32_t arg_ch, int32_t arg_10h);


    finally:
        if dlldir_handle:
            dlldir_handle.close()

