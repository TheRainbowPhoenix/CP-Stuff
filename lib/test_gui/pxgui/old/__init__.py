import ctypes

import win32gui

from . import dxapp
from lib.test_gui.pxgui.old.common.winapi import WinAPI
from lib.test_gui.pxgui.old.common import winapiconsts as w32const

from .dx9.loader import get_directx_libs
from .dx9.methods import hook_methods

def stub():
    d3d9_dll, d3dx9_43_dll = get_directx_libs()
    hwnd = hook_methods(d3d9_dll, d3dx9_43_dll)

    import ctypes

    SW_SHOW = 5
    u32 = ctypes.windll.user32
    u32.SetWindowPos(hwnd, 0, x=0, y=0, cx=200, cy=200, uFlags=0)

    ctypes.windll.user32.ShowWindow(hwnd, SW_SHOW)

    print("OK")


class Application:
    def __init__(self):
        self.active = False
        self.winapi = WinAPI()
        win32gui.InitCommonControls()
        self.window = dxapp.DirectXWindow()
        self.window.prepareClass()
        self.window.createWindow()

    def pumpMessages(self):
        msg = ctypes.wintypes.MSG()
        while self.active:
            bRet = self.winapi.user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
            if bRet == 0:  # WM_QUIT Message
                print('WM_QUIT - bye')
                # exit(0)
            elif bRet == -1:  # Error
                print('[event_loop] an error happened')
                # exit(-1)
            else:
                self.winapi.user32.TranslateMessage(ctypes.byref(msg))
                self.winapi.user32.DispatchMessageW(ctypes.byref(msg))

    def start(self):
        self.active = True
        self.window.application = self
        # self.event_loop.start()
        # self.window.show()
        win32gui.PumpMessages()

    def quit(self):
        self.active = False
        self.winapi.user32.PostQuitMessage(w32const.NULL)
        # self.event_loop.join()
