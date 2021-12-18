from ctypes import *

_WNDPROC = WINFUNCTYPE(c_long, c_int, c_uint, c_int, c_int)


def HIWORD(a): return (c_ushort)(a >> 16)


def LOWORD(a): return c_ushort(a)


class WNDCLASS(Structure):
    _fields_ = [('style', c_uint),
                ('lpfnWndProc', _WNDPROC),
                ('cbClsExtra', c_int),
                ('cbWndExtra', c_int),
                ('hInstance', c_int),
                ('hIcon', c_int),
                ('hCursor', c_int),
                ('hbrBackground', c_int),
                ('lpszMenuName', c_wchar_p),
                ('lpszClassName', c_wchar_p)]
