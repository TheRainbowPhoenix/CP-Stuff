import ctypes

import win32gui

from . import dxapp
from .common.winapi import WinAPI
from .common import winapiconsts as w32const


class Application:
    def __init__(self):
        self.active = False
        self.winapi = WinAPI()
        win32gui.InitCommonControls()
        self.window = dxapp.DirectXWindow()
        self.window.prepareClass()
        self.window.createWindow()

    def start(self):
        self.active = True
        self.window.application = self
        # win32gui.PumpMessages()
        # msg = ctypes.wintypes.MSG()

        while self.active:
            res, msg = win32gui.PeekMessage(self.window.hwnd, 0, 0, w32const.PM_REMOVE)
            win32gui.TranslateMessage(msg)
            win32gui.DispatchMessage(msg)

            if msg[1] == w32const.WM_QUIT:
                print('WM_QUIT')
                self.active = False

            self.window.render_frame()

        self.window.cleanup()
        self.quit()



    def quit(self):
        self.active = False
        self.winapi.user32.PostQuitMessage(w32const.NULL)
