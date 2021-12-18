import ctypes

from ctypes import WINFUNCTYPE, Structure
from ctypes.wintypes import *

HRESULT = DWORD

# Direct3D9 constants
D3D_SDK_VERSION = 32
D3DADAPTER_DEFAULT = 0
D3DDEVTYPE_HAL = 1
D3DDEVTYPE_REF = 2
D3DCREATE_MULTITHREADED = 0x00000004
D3DCREATE_SOFTWARE_VERTEXPROCESSING = 0x00000020
D3DCREATE_HARDWARE_VERTEXPROCESSING = 0x00000040
D3DCREATE_MIXED_VERTEXPROCESSING = 0x00000080

D3DPT_TRIANGLELIST = 4
D3DPT_TRIANGLESTRIP = 5

D3DSWAPEFFECT = UINT
D3DSWAPEFFECT_DISCARD = 1

D3DX_DEFAULT = UINT(-1)
D3DX_DEFAULT_NONPOW2 = UINT(-2)
D3DXFX_NOT_CLONEABLE = (1 << 11)
D3DXSHADER_SKIPOPTIMIZATION = (1 << 2)

D3DPOOL = UINT
D3DPOOL_DEFAULT = 0
D3DPOOL_MANAGED = 1
D3DPOOL_SYSTEMMEM = 2

D3DUSAGE_RENDERTARGET = 0x00000001
D3DUSAGE_DEPTHSTENCIL = 0x00000002
D3DUSAGE_DYNAMIC = 0x00000200

D3DCLEAR_TARGET = 0x00000001

D3DCUBEMAP_FACE_POSITIVE_X = 0
D3DCUBEMAP_FACE_NEGATIVE_X = 1
D3DCUBEMAP_FACE_POSITIVE_Y = 2
D3DCUBEMAP_FACE_NEGATIVE_Y = 3
D3DCUBEMAP_FACE_POSITIVE_Z = 4
D3DCUBEMAP_FACE_NEGATIVE_Z = 5

D3DRESOURCETYPE = UINT
D3DRTYPE_SURFACE = 1
D3DRTYPE_VOLUME = 2
D3DRTYPE_TEXTURE = 3
D3DRTYPE_VOLUMETEXTURE = 4
D3DRTYPE_CUBETEXTURE = 5
D3DRTYPE_VERTEXBUFFER = 6
D3DRTYPE_INDEXBUFFER = 7

D3DQUERYTYPE_TIMESTAMP = 10
D3DISSUE_END = (1 << 0)
D3DGETDATA_FLUSH = (1 << 0)


class D3DFORMAT:
    values = [
        ("UNKNOWN", 0),
        ("R8G8B8", 20),
        ("A8R8G8B8", 21),
        ("X8R8G8B8", 22),
        ("R5G6B5", 23),
        ("X1R5G5B5", 24),
        ("A1R5G5B5", 25),
        ("A4R4G4B4", 26),
        ("R3G3B2", 27),
        ("A8", 28),
        ("A8R3G3B2", 29),
        ("X4R4G4B4", 30),
        ("A2B10G10R10", 31),
        ("A8B8G8R8", 32),
        ("X8B8G8R8", 33),
        ("G16R16", 34),
        ("A2R10G10B10", 35),
        ("A16B16G16R16", 36),
        ("A8P8", 40),
        ("P8", 41),
        ("L8", 50),
        ("A8L8", 51),
        ("A4L4", 52),
        ("V8U8", 60),
        ("L6V5U5", 61),
        ("X8L8V8U8", 62),
        ("Q8W8V8U8", 63),
        ("V16U16", 64),
        ("A2W10V10U10", 67),
        ("L16", 81),
        ("DXT1", 0x31545844),
        ("DXT2", 0x32545844),
        ("DXT3", 0x33545844),
        ("DXT4", 0x34545844),
        ("DXT5", 0x35545844),

        # Floating point surface formats
        # s10e5 formats (16-bits per channel)
        ("R16F", 111),
        ("G16R16F", 112),
        ("A16B16G16R16F", 113),

        # IEEE s23e8 formats (32-bits per channel)
        ("R32F", 114),
        ("G32R32F", 115),
        ("A32B32G32R32F", 116),
    ]

    by_num = {}
    by_str = {}

    for x in values:
        by_num[x[1]] = x[0]
        by_str[x[0]] = x[1]


class D3DXIMAGE_FILEFORMAT:
    values = [
        ("BMP", 0),
        ("JPG", 1),
        ("TGA", 2),
        ("PNG", 3),
        ("DDS", 4),
        ("PPM", 5),
        ("DIB", 6),
        ("HDR", 7),
        ("PFM", 8),
    ]

    by_num = {}
    by_str = {}

    for x in values:
        name = x[0].lower()
        value = x[1]
        by_num[value] = name
        by_str[name] = value


D3DMULTISAMPLE_TYPE = UINT


class D3DPRESENT_PARAMETERS(Structure):
    _fields_ = [
        ('BackBufferWidth', UINT),
        ('BackBufferHeight', UINT),
        ('BackBufferFormat', UINT),  # D3DFORMAT
        ('BackBufferCount', UINT),
        ('MultiSampleType', D3DMULTISAMPLE_TYPE),
        ('MultiSampleQuality', DWORD),
        ('SwapEffect', D3DSWAPEFFECT),
        ('hDeviceWindow', HWND),
        ('Windowed', BOOL),
        ('EnableAutoDepthStencil', BOOL),
        ('AutoDepthStencilFormat', UINT),  # D3DFORMAT
        ('Flags', DWORD),
        ('FullScreen_RefreshRateInHz', UINT),
        ('PresentationInterval', UINT),
    ]


class D3DXIMAGE_INFO(Structure):
    _fields_ = [
        ('Width', UINT),
        ('Height', UINT),
        ('Depth', UINT),
        ('MipLevels', UINT),
        ('Format', UINT),  # D3DFORMAT
        ('ResourceType', D3DRESOURCETYPE),
        ('ImageFileFormat', UINT),  # D3DXIMAGE_FILEFORMAT
    ]


class D3DSURFACE_DESC(Structure):
    _fields_ = [
        ('Format', UINT),  # D3DFORMAT
        ('Type', D3DRESOURCETYPE),
        ('Usage', DWORD),
        ('Pool', D3DPOOL),
        ('MultiSampleType', D3DMULTISAMPLE_TYPE),
        ('MultiSampleQuality', DWORD),
        ('Width', UINT),
        ('Height', UINT),
    ]


class D3DVOLUME_DESC(Structure):
    _fields_ = [
        ('Format', UINT),  # D3DFORMAT
        ('Type', D3DRESOURCETYPE),
        ('Usage', DWORD),
        ('Pool', D3DPOOL),
        ('Width', UINT),
        ('Height', UINT),
        ('Depth', UINT),
    ]


class D3DXVECTOR4(Structure):
    _fields_ = [
        ('x', FLOAT), ('y', FLOAT), ('z', FLOAT), ('w', FLOAT),
    ]


class TRI_VTX(Structure):
    FVF = 0x00000104  # D3DFVF_XYZRHW | D3DFVF_TEXCOORDSIZE2( 0 ) | D3DFVF_TEX1
    _fields_ = [
        ('x0', FLOAT), ('y0', FLOAT), ('z0', FLOAT), ('w0', FLOAT), ('u0', FLOAT), ('v0', FLOAT),
        ('x1', FLOAT), ('y1', FLOAT), ('z1', FLOAT), ('w1', FLOAT), ('u1', FLOAT), ('v1', FLOAT),
        ('x2', FLOAT), ('y2', FLOAT), ('z2', FLOAT), ('w2', FLOAT), ('u2', FLOAT), ('v2', FLOAT),
    ]


class QUAD_VTX(Structure):
    FVF = 0x00000104  # D3DFVF_XYZRHW | D3DFVF_TEXCOORDSIZE2( 0 ) | D3DFVF_TEX1
    _fields_ = [
        ('x0', FLOAT), ('y0', FLOAT), ('z0', FLOAT), ('w0', FLOAT), ('u0', FLOAT), ('v0', FLOAT),
        ('x1', FLOAT), ('y1', FLOAT), ('z1', FLOAT), ('w1', FLOAT), ('u1', FLOAT), ('v1', FLOAT),
        ('x2', FLOAT), ('y2', FLOAT), ('z2', FLOAT), ('w2', FLOAT), ('u2', FLOAT), ('v2', FLOAT),
        ('x3', FLOAT), ('y3', FLOAT), ('z3', FLOAT), ('w3', FLOAT), ('u3', FLOAT), ('v3', FLOAT),
    ]


# D3D9 Function Prototypes
COM_Release = WINFUNCTYPE(UINT)(2, "COM_Release")
D3D9_CreateDevice = WINFUNCTYPE(HRESULT, UINT, UINT, HWND, DWORD, LPVOID, LPVOID)(16, "D3D9_CreateDevice")
IDirect3DDevice9_CreateTexture = WINFUNCTYPE(HRESULT, UINT, UINT, UINT, DWORD, UINT, UINT, LPVOID, LPVOID)(23,
                                                                                                           "IDirect3DDevice9_CreateTexture")
IDirect3DDevice9_CreateVolumeTexture = WINFUNCTYPE(HRESULT, UINT, UINT, UINT, UINT, DWORD, UINT, UINT, LPVOID, LPVOID)(
    24, "IDirect3DDevice9_CreateVolumeTexture")
IDirect3DDevice9_CreateCubeTexture = WINFUNCTYPE(HRESULT, UINT, UINT, DWORD, UINT, UINT, LPVOID, LPVOID)(25,
                                                                                                         "IDirect3DDevice9_CreateCubeTexture")
IDirect3DDevice9_SetRenderTarget = WINFUNCTYPE(HRESULT, DWORD, LPVOID)(37, "IDirect3DDevice9_SetRenderTarget")
IDirect3DDevice9_BeginScene = WINFUNCTYPE(HRESULT)(41, "IDirect3DDevice9_BeginScene")
IDirect3DDevice9_EndScene = WINFUNCTYPE(HRESULT)(42, "IDirect3DDevice9_EndScene")
# device, source, dest, override, dirty);
IDirect3DDevice9_Present = WINFUNCTYPE(HRESULT, LPRECT, LPRECT, HWND, LPVOID)(42, "IDirect3DDevice9_Present")
IDirect3DDevice9_Clear = WINFUNCTYPE(HRESULT, DWORD, LPVOID, DWORD, DWORD, FLOAT, DWORD)(43, "IDirect3DDevice9_Clear")
IDirect3DDevice9_DrawPrimitiveUP = WINFUNCTYPE(HRESULT, UINT, UINT, LPVOID, UINT)(83, "IDirect3DDevice9_DrawPrimitive")
IDirect3DDevice9_DrawPrimitive = WINFUNCTYPE(HRESULT, UINT, UINT, UINT)(84, "IDirect3DDevice9_DrawPrimitive")
IDirect3DDevice9_SetFVF = WINFUNCTYPE(HRESULT, DWORD)(89, "IDirect3DDevice9_SetFVF")
IDirect3DDevice9_CreateQuery = WINFUNCTYPE(HRESULT, DWORD, LPVOID)(118, "IDirect3DDevice9_CreateQuery")
IDirect3DQuery9_Issue = WINFUNCTYPE(HRESULT, DWORD)(6, "IDirect3DQuery9_Issue")
IDirect3DQuery9_GetData = WINFUNCTYPE(HRESULT, LPVOID, DWORD, DWORD)(7, "IDirect3DQuery9_GetData")
Direct3DBaseTexture9_GetType = WINFUNCTYPE(DWORD)(10, "Direct3DBaseTexture9_GetType")
Direct3DBaseTexture9_GetLevelCount = WINFUNCTYPE(DWORD)(13, "Direct3DBaseTexture9_GetLevelCount")
IDirect3DTexture9_GetLevelDesc = WINFUNCTYPE(DWORD, UINT, LPVOID)(17, "IDirect3DTexture9_GetLevelDesc")
IDirect3DTexture9_GetSurfaceLevel = WINFUNCTYPE(DWORD, UINT, LPVOID)(18, "IDirect3DTexture9_GetSurfaceLevel")
IDirect3DCubeTexture9_GetLevelDesc = WINFUNCTYPE(DWORD, UINT, LPVOID)(17, "IDirect3DCubeTexture9_GetLevelDesc")
IDirect3DCubeTexture9_GetCubeMapSurface = WINFUNCTYPE(DWORD, UINT, UINT, LPVOID)(18,
                                                                                 "IDirect3DCubeTexture9_GetCubeMapSurface")
IDirect3DVolumeTexture9_GetLevelDesc = WINFUNCTYPE(DWORD, UINT, LPVOID)(17, "IDirect3DVolumeTexture9_GetLevelDesc")
D3DXBUFFER_GetBufferPointer = WINFUNCTYPE(LPVOID)(3, "D3DXBUFFER_GetBufferPointer")
D3DXBUFFER_GetBufferSize = WINFUNCTYPE(DWORD)(4, "D3DXBUFFER_GetBufferSize")
ID3DXEffect_SetFloat = WINFUNCTYPE(HRESULT, LPCSTR, FLOAT)(30, "ID3DXEffect_SetFloat")
ID3DXEffect_SetVector = WINFUNCTYPE(HRESULT, LPCSTR, LPVOID)(34, "ID3DXEffect_SetVector")
ID3DXEffect_SetTexture = WINFUNCTYPE(HRESULT, LPCSTR, LPVOID)(52, "ID3DXEffect_SetTexture")
ID3DXEffect_SetTechnique = WINFUNCTYPE(HRESULT, LPCSTR)(58, "ID3DXEffect_SetTechnique")
ID3DXEffect_Begin = WINFUNCTYPE(HRESULT, LPVOID, DWORD)(63, "ID3DXEffect_Begin")
ID3DXEffect_BeginPass = WINFUNCTYPE(HRESULT, UINT)(64, "ID3DXEffect_BeginPass")
ID3DXEffect_EndPass = WINFUNCTYPE(HRESULT)(66, "ID3DXEffect_EndPass")
ID3DXEffect_End = WINFUNCTYPE(HRESULT)(67, "ID3DXEffect_End")

# Windows constants
CreateWindowEx = ctypes.windll.user32.CreateWindowExA
CreateWindowEx.argtypes = [DWORD, LPCSTR, LPCSTR, DWORD, UINT, UINT, UINT, UINT, HWND, HMENU, HINSTANCE, LPVOID]
CreateWindowEx.restype = HWND

WS_OVERLAPPEDWINDOW = 0x00CF0000


# Colors
class D3DCOLOR_XRGB(Structure):
    _fields_ = [
        ('r', UINT),
        ('g', UINT),
        ('b', UINT),
    ]


class Vertex(Structure):
    _fields_ = [
        ('x', FLOAT),
        ('y', FLOAT),
        ('z', FLOAT),
        ('rhw', FLOAT),
        ('diffuse', DWORD),
    ]
