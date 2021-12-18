from ctypes import windll


class WinAPI:
    """
    Windows API wrapper
    """

    def __init__(self):
        self._user32 = None
        self._comctl32 = None
        self._kernel32 = None
        self._uxtheme = None
        self._atl = None
        self._gdi32 = None

    @staticmethod
    def _try_dll(dll_name: str):
        """
        Try to load a dll
        :param dll_name: dll name without the ".dll"
        :return: dll instance
        :raise FileNotFoundError: if file cannot be found
        """
        try:
            dll_inst = windll.LoadLibrary(dll_name)
            return dll_inst
        except Exception:
            raise FileNotFoundError(f"Cannot load DLL \"{dll_name}\"")

    @property
    def user32(self):
        if not self._user32:
            self._user32 = self._try_dll("user32")
        return self._user32

    @property
    def comctl32(self):
        if not self._comctl32:
            self._comctl32 = self._try_dll("comctl32")
        return self._comctl32

    @property
    def kernel32(self):
        if not self._kernel32:
            self._kernel32 = self._try_dll("kernel32")
        return self._kernel32

    @property
    def uxtheme(self):
        if not self._uxtheme:
            self._uxtheme = self._try_dll("UxTheme")
        return self._uxtheme

    @property
    def atl(self):
        if not self._atl:
            self._atl = self._try_dll("atl")
        return self._atl

    @property
    def gdi32(self):
        if not self._gdi32:
            self._gdi32 = self._try_dll("gdi32")
        return self._gdi32


