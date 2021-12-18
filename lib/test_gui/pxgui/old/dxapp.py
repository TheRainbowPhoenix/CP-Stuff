from timer import set_timer, kill_timer

from win32gui import SetWindowLong, SetWindowPos, ShowWindow

from lib.test_gui.pxgui.common.window import BaseWindow
from lib.test_gui.pxgui.common.message import subscriber, subscribe
# from .common import winapiconsts as w32const
from .old.common import win32structs
from .old.common.winapiconsts import *

from .utils import get_message_name


@subscriber
class DirectXWindow(BaseWindow):
    def __init__(self):
        BaseWindow.__init__(self)
        self._mofidier = 0

    @subscribe
    def on_message(self, hwnd, message, wparam, lparam):
        print("[%d] message=%-24s wparam=0x%08x lparam=0x%08x" % (hwnd, get_message_name(message), wparam, lparam))

    @subscribe(WM_CREATE)
    def on_create(self, hwnd, message, wparam, lparam):
        set_timer(3000, self.on_timer)
        width = win32structs.LOWORD(lparam)
        height = win32structs.HIWORD(lparam)

        # SetWindowLong(hwnd, GWL_STYLE, WS_POPUP | WS_CHILD)
        # SetWindowLong(hwnd, GWL_EXSTYLE, WS_EX_LAYERED | WS_EX_TOPMOST | WS_EX_TOOLWINDOW)
        # SetWindowPos(self.hwnd, 0, 0, 0, 200, 200, SWP_NOMOVE | SWP_NOZORDER)
        # SetWindowPos(self.hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
        # SetWindowPos(self.hwnd, 0, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOZORDER)

        # SetWindowPos(hwnd, HWND_TOP, 0, 0, width.value, height.value, SWP_SHOWWINDOW)
        ShowWindow(self.hwnd, SW_SHOW)

    @subscribe(WM_LBUTTONDOWN, WM_RBUTTONDOWN, WM_MBUTTONDOWN)
    def on_mousedown(self, hwnd, message, wparam, lparam):
        # dx, dy = (lparam & 0xFFFF, lparam >> 16)
        dx = win32structs.LOWORD(lparam)
        dy = win32structs.HIWORD(lparam)
        print(f"on_mousedown @ {dx}:{dy}")

    @subscribe(WM_LBUTTONUP, WM_RBUTTONUP, WM_MBUTTONUP)
    def on_mouseup(self, hwnd, message, wparam, lparam):
        if wparam & (MK_LBUTTON | MK_MBUTTON | MK_RBUTTON) == 0:
            print("Mouse Released")

    @subscribe(WM_MOUSEMOVE)
    def on_mousemove(self, hwnd, message, wparam, lparam):
        if wparam & MK_LBUTTON:
            x0, y0 = self.winapi.user32.GetCursorPos()

            print(f"MouseMove @ {x0}:{y0}")

    @subscribe(WM_PAINT)
    def do_paint(self, hwnd, message, wparam, lparam):
        pass

    @subscribe(WM_DESTROY)
    def on_destroy(self, hwnd, message, wparam, lparam):
        self.application.quit()
        
    def on_timer(self, timer_id, time):
        kill_timer(timer_id)
        print("TimeOut !!")
        # self.destroyWindow()