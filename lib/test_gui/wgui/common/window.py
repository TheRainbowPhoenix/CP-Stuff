import win32gui
import win32api
import win32con

class BaseWindow(object):

    def __init__(self, hInstance=win32gui.dllhandle):
        self._wm_create_subscriptions = [] # workaround WM_CREATE problem
        self.application = None
        self.hInstance = hInstance
        self.className = self.__class__.__name__
        self.hwnd = None

    def prepareClass(self, hcursor=0, hicon=0, style=win32con.CS_HREDRAW|win32con.CS_VREDRAW):
        wc = win32gui.WNDCLASS()
        wc.lpszClassName = self.className
        wc.lpfnWndProc = self.get_wnd_proc()
        wc.hInstance = self.hInstance
        if not hcursor:
            hcursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        wc.hCursor = hcursor
        wc.hIcon = hicon
        wc.hbrBackground = win32con.COLOR_WINDOW + 1
        wc.style = style
        return win32gui.RegisterClass(wc)

    def createWindow(self,
            title='No Name',
            style=win32con.WS_CAPTION|win32con.WS_SYSMENU,
            x=win32con.CW_USEDEFAULT, y=win32con.CW_USEDEFAULT,
            w=win32con.CW_USEDEFAULT, h=win32con.CW_USEDEFAULT):
        self.hwnd = win32gui.CreateWindow(
                self.className, title, style, x, y, w, h, 0, 0,
                self.hInstance, None)
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
                 |win32con.SWP_NOSIZE):
        return win32gui.SetWindowPos(self.hwnd, z, x, y, w, h, flags)

    def show(self, cmdShow = win32con.SW_SHOW):
        return win32gui.ShowWindow(self.hwnd, cmdShow)

