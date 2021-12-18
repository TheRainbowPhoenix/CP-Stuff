import win32gui
from . import winapp


class Application:
    def __init__(self):
        win32gui.InitCommonControls()
        self.window = winapp.OverlayWindow()
        self.window.prepareClass()
        self.window.createWindow()

    def start(self):
        self.window.application = self
        win32gui.PumpMessages()

    def quit(self):
        win32gui.PostQuitMessage(0)
