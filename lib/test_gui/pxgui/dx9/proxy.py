import atexit
from ctypes import sizeof

from .loader import get_directx_libs
from .methods import hook_methods

from .types import *


def stub():
    d3d9_dll, d3dx9_43_dll = get_directx_libs()
    hwnd = hook_methods(d3d9_dll, d3dx9_43_dll)

    import ctypes

    SW_SHOW = 5
    u32 = ctypes.windll.user32
    u32.SetWindowPos(hwnd, 0, x=0, y=0, cx=200, cy=200, uFlags=0)

    ctypes.windll.user32.ShowWindow(hwnd, SW_SHOW)

    print("OK")


class DirectXProxy:
    def __init__(self):
        self.d3_dll = None
        self.d3dx_dll = None

        self.d3ddev = None  # pointer to the device class
        self.d3d = None  # pointer to Direct3D interface
        self.lpFlushQuery = None

    def load_libs(self):
        self.d3_dll, self.d3dx_dll = get_directx_libs()

    def register_functions(self):
        hook_methods(self, self.d3_dll, self.d3dx_dll)

    def Direct3DCreate9(self, version):
        raise NotImplementedError("Direct3DCreate9 is not implemented. Did you call \"register_functions()\" ?")

    def init_d3d(self, hwnd):
        # Initialize Direct3D
        self.d3d = LPVOID(self.Direct3DCreate9(D3D_SDK_VERSION))

        if not self.d3d:
            raise Exception("Failed to create D3D")

        # hWnd = CreateWindowEx(0, "STATIC".encode("ascii"), "fxproc_window".encode("ascii"), WS_OVERLAPPEDWINDOW, 0, 0,
        #                       100,
        #                       100, 0, 0, 0, 0)

        if hwnd == 0:
            raise Exception("Failed to create window")

        NULL = LPVOID(0)
        self.d3ddev = LPVOID(0)
        d3dpp = D3DPRESENT_PARAMETERS(Windowed=1, SwapEffect=D3DSWAPEFFECT_DISCARD, hwnd=hwnd)

        try:
            D3D9_CreateDevice(self.d3d, D3DADAPTER_DEFAULT, D3DDEVTYPE_HAL, hwnd,
                              D3DCREATE_MULTITHREADED | D3DCREATE_HARDWARE_VERTEXPROCESSING,
                              ctypes.byref(d3dpp),
                              ctypes.byref(self.d3ddev))

        #:TODO: Try different configurations when one fails
        # D3D9_CreateDevice(lpD3D9, D3DADAPTER_DEFAULT, D3DDEVTYPE_HAL, hWnd, D3DCREATE_SOFTWARE_VERTEXPROCESSING, ctypes.byref(d3dpp), ctypes.byref(lpDevice))
        # D3D9_CreateDevice(lpD3D9, D3DADAPTER_DEFAULT, D3DDEVTYPE_REF, hWnd, D3DCREATE_HARDWARE_VERTEXPROCESSING, ctypes.byref(d3dpp), ctypes.byref(lpDevice))
        except Exception:
            raise Exception("Failed to create D3D device")

        self.lpFlushQuery = LPVOID(0)
        try:
            IDirect3DDevice9_CreateQuery(self.d3ddev, D3DQUERYTYPE_TIMESTAMP, ctypes.byref(self.lpFlushQuery))
        except Exception:
            pass

        return hwnd

    def cleanup(self):
        if self.lpFlushQuery:
            COM_Release(self.lpFlushQuery)

        ref = 0

        if self.d3ddev:
            ref += COM_Release(self.d3ddev)

        if self.d3d:
            ref += COM_Release(self.d3d)

        if ref != 0:
            print("WARNING: leaking D3D resources")

    def getVertex(self, points2d):
        vertexes = (Vertex * len(points2d))()
        for i, (x, y, c) in enumerate(points2d):
            vertexes[i] = Vertex(x, y, 0, 1, c)

        return vertexes

    def render_frame(self):
        """
            [in] DWORD         Count,
            [in] const D3DRECT *pRects,
            [in] DWORD         Flags,
            [in] D3DCOLOR      Color,
            [in] float         Z,
            [in] DWORD         Stencil
        """
        # TODO: D3DCOLOR_XRGB(0, 40, 100) return 0xFFFFFF color
        IDirect3DDevice9_Clear(self.d3ddev, 0, None, D3DCLEAR_TARGET, 0xFF00FF, 0.0, 0)
        IDirect3DDevice9_BeginScene(self.d3ddev)


        vertex = self.getVertex(((0, 0, 0),) * 4)
        IDirect3DDevice9_DrawPrimitive(self.d3ddev, D3DPT_TRIANGLESTRIP, 0, 6)
        # IDirect3DDevice9_DrawPrimitiveUP(self.d3ddev, D3DPT_TRIANGLESTRIP, 2, vertex, sizeof(Vertex))

        IDirect3DDevice9_EndScene(self.d3ddev)
        IDirect3DDevice9_Present(self.d3ddev, None, None, None, None)
