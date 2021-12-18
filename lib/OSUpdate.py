"""
OS Update reversed

"C:\Windows\SysWOW64\rundll32.exe" "OSupdateDLL.dll", OSUpdate

fxASPI (Advanced SCSI Programing Interface):
    - fxASPI_Init
    - fxASPI_GetDeviceNum
    - fxASPI_writeData

    - fxASPI_Init
    - (loop ?) Error message


LanguageResource (messages displayed)
    - InitLanguageResource()
    - GetLangMessage
"""

import sys, ctypes, platform, os, re


if platform.system().lower() == 'windows':
    import os.path

    dll_name = "LanguageResource.dll"

    current_path = os.path.abspath(os.path.dirname(__file__))

    dlldir_handle = None
    dll_path = os.path.dirname(os.path.abspath(__file__)) + os.path.sep

    os.environ['path'] = current_path + ';' + os.environ['path']
    sys.path.insert(0, current_path)
    if sys.version_info >= (3, 8):
        dlldir_handle = os.add_dll_directory(current_path)


    def errcheck(result, func, args):
        if not result:
            print("errcheck: no result !")
            raise ctypes.WinError()
        return args

    try:

        # language_resource_dll = ctypes.WinDLL(dll_name, winmode=0)
        # initLanguageResource = language_resource_dll.InitLanguageResource
        # initLanguageResource.restype = ctypes.c_int
        # initLanguageResource.argtypes = []
        #
        # getLangMessage = language_resource_dll.GetLangMessage
        # getLangMessage.restype = ctypes.c_int
        # getLangMessage.argtypes = [ctypes.c_int32, ctypes.c_wchar_p]


        language_resource_lib = ctypes.windll.LoadLibrary(dll_name)
        language_resource_dll = ctypes.WinDLL(dll_name, winmode=0)

        # try:
        #     init = initLanguageResource()
        #
        #     base_msg = ctypes.c_wchar_p()
        #     msg = getLangMessage(2, base_msg)
        #
        # except WindowsError as e:
        #     print("WindowsError")
        #     print(e)
        # except Exception as e:
        #     print(e)

        UINT_PTR = ctypes.POINTER(ctypes.c_uint)

        # InitLanguageResource() -> int | bool
        # 0x10001030, ord 2
        init = language_resource_lib.InitLanguageResource()
        print(init)

        # GetLangMessage (int32_t arg_8h, int32_t address) -> int
        # Address is relative, 4*address+0x100053b0
        # 0x100053b0
        # 0x82 do nothing
        #
        # language_resource_lib.GetLangMessage.argtypes = [ctypes.wintypes.DWORD, ctypes.c_wchar_p]
        language_resource_lib.GetLangMessage.errcheck = errcheck

        # 0x1a => "Welcome to Hook2!"
        # 0x02 => "Connect the calculator"
        #
        base_msg = ctypes.create_string_buffer(514)
        base_msg_ptr = (ctypes.c_wchar_p)(ctypes.addressof(base_msg))
        base_id = ctypes.c_uint(2)
        # base_id * 4 + 0x100053b0
        msg = language_resource_lib.GetLangMessage(base_id, base_msg_ptr)
        # out = base_msg.raw.replace(b'\x00', b'')
        print(base_msg.raw.decode('utf-16').replace('\x00', ''))

        # Bruteforce str
        for i in range(0, 26):
            try:
                base_msg = ctypes.create_string_buffer(514)
                base_msg_ptr = (ctypes.c_wchar_p)(ctypes.addressof(base_msg))
                base_id = ctypes.c_uint(i)
                msg = language_resource_lib.GetLangMessage(base_id, base_msg_ptr)
                out = base_msg.raw.decode("utf-16").replace("\x00", "")
                prnt_out = out.encode("unicode_escape").decode("utf-8")
                print(f"ID: {i}\t : " + fr'{prnt_out}')
            except:
                print(f"ID: {i}\t : == !! Error !! ==")


    finally:
        if dlldir_handle:
            dlldir_handle.close()



