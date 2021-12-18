import ctypes

import win32gui

from .winapi import WinAPI
from . import winapiconsts as w32const

from . import types
from .win32structs import WNDCLASS, _WNDPROC, LOWORD, HIWORD


class BaseWindow(object):
    def __init__(self):
        self.instance = self
        self.winapi = WinAPI()
        self.application = None
        self.className = self.__class__.__name__
        self.hwnd = None
        self.hInstance = self.winapi.kernel32.GetModuleHandleA(None)

    def prepareClass(self, hcursor=w32const.NULL, hicon=w32const.NULL, style=w32const.CS_HREDRAW | w32const.CS_VREDRAW):
        wndclass = WNDCLASS()
        wndclass.style = style
        wndclass.lpfnWndProc = self._get_wnd_proc()
        wndclass.cbClsExtra = wndclass.cbWndExtra = 0
        wndclass.hInstance = self.hInstance
        if not hcursor:
            hcursor = self.winapi.user32.LoadCursorW(ctypes.c_int(w32const.NULL), ctypes.c_int(w32const.IDC_ARROW))
        wndclass.hCursor = hcursor

        if not hicon:
            hicon = self.winapi.user32.LoadIconW(ctypes.c_int(w32const.NULL), ctypes.c_int(w32const.IDI_APPLICATION))
        wndclass.hIcon = hicon

        # wndclass.hbrBackground = w32const.COLOR_WINDOW + 1
        wndclass.hbrBackground = self.winapi.gdi32.GetStockObject(ctypes.c_int(w32const.WHITE_BRUSH))
        wndclass.lpszMenuName = None
        wndclass.lpszClassName = self.className

        # Register Window Class
        if not self.winapi.user32.RegisterClassW(ctypes.byref(wndclass)):
            raise ctypes.WinError()

    def createWindow(self,
                     title='Untitled Window',
                     style=w32const.WS_CAPTION | w32const.WS_SYSMENU,
                     x=w32const.CW_USEDEFAULT, y=w32const.CW_USEDEFAULT,
                     w=w32const.CW_USEDEFAULT, h=w32const.CW_USEDEFAULT
                     ) -> types.HWND:
        """
        Create a new window using user32::CreateWindow
        :param title: Window Title
        :param style: Window style flags
        :param x: Window position (x)
        :param y: Window position (y)
        :param w: Window width
        :param h: Window height
        :return: HWND pointer
        """
        # self.hwnd = self.winapi.user32.CreateWindow(
        #     self.className, title, style, x, y, w, h, w32const.NULL, w32const.NULL,
        # )
        """
        HWND CreateWindowExW(
            DWORD dwExStyle, // extended window style
            LPCTSTR lpClassName, // pointer to registered class name
            LPCTSTR lpWindowName, // pointer to window name
            DWORD dwStyle, // window style
            int x, // horizontal position of window
            int y, // vertical position of window
            int nWidth, // window width
            int nHeight, // window height
            HWND hWndParent, // handle to parent or owner window
            HMENU hMenu, // handle to menu, or child-window identifier
            HINSTANCE hInstance, // handle to application instance
            LPVOID lpParam // pointer to window-creation data
        );
        """
        dwExStyle = w32const.WS_OVERLAPPEDWINDOW
        hWndParent = w32const.NULL
        hMenu = w32const.NULL
        lpParam = None
        self.hwnd = self.winapi.user32.CreateWindowExW(
            dwExStyle, self.className, title, style, x, y, w, h,
            hWndParent, hMenu, self.hInstance, lpParam
        )

        try:
            self.winapi.user32.SetProcessDPIAware()
            self.winapi.uxtheme.SetWindowTheme(self.hwnd, "DarkMode_Explorer", w32const.NULL)
        except Exception as e:
            print(e)

        # self.winapi.user32.SendMessageW(self.hwnd, w32const.WM_CREATE, w32const.NULL, w32const.NULL)
        win32gui.SendMessage(self.hwnd, w32const.WM_CREATE, 0, 0)
        return self.hwnd

    def destroyWindow(self):
        return self.winapi.user32.DestroyWindow(self.hwnd)

    def setWindowLong(self, index, value):
        return self.winapi.user32.SetWindowLong(self.hwnd, index, value)

    def getWindowLong(self, index):
        return self.winapi.user32.GetWindowLong(self.hwnd, index)

    def setWindowPos(self,
                     z=0, x=0, y=0, w=0, h=0,
                     flags=w32const.SWP_NOMOVE | w32const.SWP_NOSIZE):
        return self.winapi.user32.SetWindowPos(self.hwnd, z, x, y, w, h, flags)

    def show(self, cmdShow=w32const.SW_SHOW):
        return self.winapi.user32.ShowWindow(self.hwnd, cmdShow)

    def _get_wnd_proc(self):
        if hasattr(self, 'get_wnd_proc'):
            return _WNDPROC(self.get_wnd_proc())
        else:
            def defaultWndProc(hwnd, message, wParam, lParam):
                if message == w32const.WM_SIZE:
                    # Resize the ATL window as the size of the main window is changed
                    if self.instance is not None:
                        hwnd = self.hwnd
                        width = LOWORD(lParam)
                        height = HIWORD(lParam)
                        self.winapi.user32.SetWindowPos(hwnd, w32const.HWND_TOP, 0, 0, width, height, w32const.SWP_SHOWWINDOW)
                        self.winapi.user32.ShowWindow(ctypes.c_int(hwnd), ctypes.c_int(w32const.SW_SHOW))
                        self.winapi.user32.UpdateWindow(ctypes.c_int(hwnd))
                    return 0

                elif message == w32const.WM_ERASEBKGND:
                    # Prevent flickering when resizing
                    return 0

                elif message == w32const.WM_CREATE:
                    pass  # document = BrowserView.instance.browser.Document.QueryInterface(ICustomDoc).SetUIHandler()

                elif message == w32const.WM_DESTROY:
                    self.winapi.user32.PostQuitMessage(0)
                    return 0

                return self.winapi.user32.DefWindowProcW(ctypes.c_int(hwnd), ctypes.c_int(message), ctypes.c_int(wParam), ctypes.c_int(lParam))

            return _WNDPROC(defaultWndProc)

