import ctypes


def get_directx_libs():
    """
    Check the system for any d3d9 dll and return its instance
    :return: d3d9, d3dx9
    """
    d3d9_dll = ctypes.windll.LoadLibrary('d3d9.dll')

    d3dx9_43_dll = None
    d3dx9_43_warning = False

    for d3dx_version in range(43, 31, -1):
        try:
            d3dx9_43_dll = ctypes.windll.LoadLibrary('d3dx9_%d.dll' % (d3dx_version))
            break
        except WindowsError:
            d3dx9_43_warning = True

    if not d3dx9_43_dll:
        raise Exception("Failed to find d3dx9_*.dll")

    return d3d9_dll, d3dx9_43_dll
