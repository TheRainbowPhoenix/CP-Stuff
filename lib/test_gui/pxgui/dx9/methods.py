import atexit

from .types import *


def hook_methods(module, d3d9_dll, d3dx9_43_dll):
    Direct3DCreate9 = getattr(d3d9_dll, 'Direct3DCreate9')
    Direct3DCreate9.restype = LPVOID
    setattr(module, 'Direct3DCreate9', Direct3DCreate9)

    D3DXCreateEffectFromFile = getattr(d3dx9_43_dll, 'D3DXCreateEffectFromFileA')
    D3DXCreateEffectFromFile.argtypes = [LPVOID, LPCSTR, LPVOID, LPVOID, DWORD, LPVOID, LPVOID, LPVOID]
    D3DXCreateEffectFromFile.restype = HRESULT
    setattr(module, 'D3DXCreateEffectFromFileA', D3DXCreateEffectFromFile)

    D3DXCreateEffect = getattr(d3dx9_43_dll, 'D3DXCreateEffect')
    D3DXCreateEffect.argtypes = [LPVOID, LPCSTR, UINT, LPVOID, LPVOID, DWORD, LPVOID, LPVOID, LPVOID]
    D3DXCreateEffect.restype = HRESULT
    setattr(module, 'D3DXCreateEffect', D3DXCreateEffect)

    D3DXGetImageInfoFromFile = getattr(d3dx9_43_dll, 'D3DXGetImageInfoFromFileA')
    D3DXGetImageInfoFromFile.argtypes = [LPCSTR, LPVOID]
    D3DXGetImageInfoFromFile.restype = HRESULT
    setattr(module, 'D3DXGetImageInfoFromFileA', D3DXGetImageInfoFromFile)

    D3DXCreateTextureFromFileEx = getattr(d3dx9_43_dll, 'D3DXCreateTextureFromFileExA')
    D3DXCreateTextureFromFileEx.argtypes = [LPVOID, LPCSTR, UINT, UINT, UINT, DWORD, UINT, UINT, DWORD, DWORD, UINT,
                                            LPVOID, LPVOID, LPVOID]
    D3DXCreateTextureFromFileEx.restype = HRESULT
    setattr(module, 'D3DXCreateTextureFromFileExA', D3DXCreateTextureFromFileEx)

    D3DXCreateCubeTextureFromFileEx = getattr(d3dx9_43_dll, 'D3DXCreateCubeTextureFromFileExA')
    D3DXCreateCubeTextureFromFileEx.argtypes = [LPVOID, LPCSTR, UINT, UINT, DWORD, UINT, UINT, DWORD, DWORD, UINT,
                                                LPVOID, LPVOID, LPVOID]
    D3DXCreateCubeTextureFromFileEx.restype = HRESULT
    setattr(module, 'D3DXCreateCubeTextureFromFileExA', D3DXCreateCubeTextureFromFileEx)

    D3DXSaveTextureToFile = getattr(d3dx9_43_dll, 'D3DXSaveTextureToFileA')
    D3DXSaveTextureToFile.argtypes = [LPCSTR, UINT, LPVOID, LPVOID]
    D3DXSaveTextureToFile.restype = HRESULT
    setattr(module, 'D3DXSaveTextureToFileA', D3DXSaveTextureToFile)







