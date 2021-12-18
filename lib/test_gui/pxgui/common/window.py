import ctypes

import win32gui

import win32con

from .winapi import WinAPI
from .win32structs import WNDCLASS, _WNDPROC, LOWORD, HIWORD
from . import winapiconsts as w32const

from . import types as wintypes


class BaseWindow(object):

    def __init__(self, hInstance=win32gui.dllhandle):
        self._wm_create_subscriptions = []  # workaround WM_CREATE problem
        self.application = None
        self.hInstance = hInstance
        self.className = self.__class__.__name__
        self.hwnd = None

        self.winapi = WinAPI()

    def prepareClass(self, hcursor=0, hicon=0, style=win32con.CS_HREDRAW | win32con.CS_VREDRAW):
        """
        Prepare Window for creation
        :param hcursor: default cursor
        :param hicon: default icon
        :param style: styles flag
        :return:
        """
        wndclass = win32gui.WNDCLASS()
        wndclass.style = style
        wndclass.lpfnWndProc = self.get_wnd_proc()
        # wndclass.cbClsExtra = wndclass.cbWndExtra = 0
        wndclass.hInstance = self.hInstance
        if not hcursor:
            hcursor = self.winapi.user32.LoadCursorW(ctypes.c_int(w32const.NULL), ctypes.c_int(w32const.IDC_ARROW))
        wndclass.hCursor = hcursor

        if not hicon:
            hicon = self.winapi.user32.LoadIconW(ctypes.c_int(w32const.NULL), ctypes.c_int(w32const.IDI_APPLICATION))
        wndclass.hIcon = hicon

        # wndclass.hbrBackground = w32const.COLOR_WINDOW + 1
        # wndclass.hbrBackground = self.winapi.gdi32.GetStockObject(ctypes.c_int(w32const.GRAY_BRUSH))
        # wndclass.lpszMenuName = None
        wndclass.lpszClassName = self.className

        # Register Window Class
        register = win32gui.RegisterClass(wndclass)
        if not register:
            raise ctypes.WinError()
        return register

    def createWindow(self,
                     title='PyX GUI Window',
                     style=win32con.WS_OVERLAPPEDWINDOW, # win32con.WS_CAPTION | win32con.WS_SYSMENU,
                     x=win32con.CW_USEDEFAULT, y=win32con.CW_USEDEFAULT,
                     # w=win32con.CW_USEDEFAULT, h=win32con.CW_USEDEFAULT):
                     w=800, h=600) -> wintypes.HWND:
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
        dwExStyle = w32const.NULL
        hWndParent = w32const.NULL
        hMenu = w32const.NULL
        lpParam = None

        """
        HWND CreateWindowExW(
           DWORD dwExStyle,         // extended window style
           LPCTSTR lpClassName,     // pointer to registered class name
           LPCTSTR lpWindowName,    // pointer to window name
           DWORD dwStyle,           // window style
           int x,                   // horizontal position of window
           int y,                   // vertical position of window
           int nWidth,              // window width
           int nHeight,             // window height
           HWND hWndParent,         // handle to parent or owner window
           HMENU hMenu,             // handle to menu, or child-window identifier
           HINSTANCE hInstance,     // handle to application instance
           LPVOID lpParam           // pointer to window-creation data
        );
        """
        self.hwnd = win32gui.CreateWindowEx(
            dwExStyle, self.className, title, style, x, y, w, h,
            hWndParent, hMenu, self.hInstance, lpParam
        )
        win32gui.SendMessage(self.hwnd, win32con.WM_CREATE, 0, 0)
        return self.hwnd

    def destroyWindow(self):
        return win32gui.DestroyWindow(self.hwnd)

    def setWindowLong(self, index, value):
        return win32gui.SetWindowLong(self.hwnd, index, value)

    def getWindowLong(self, index):
        return win32gui.GetWindowLong(self.hwnd, index)

    def setWindowPos(self,
                     z=0, x=0, y=0, w=0, h=0,
                     flags=win32con.SWP_NOMOVE
                           | win32con.SWP_NOSIZE):
        return win32gui.SetWindowPos(self.hwnd, z, x, y, w, h, flags)

    def show(self, cmdShow=win32con.SW_SHOW):
        return win32gui.ShowWindow(self.hwnd, cmdShow)
