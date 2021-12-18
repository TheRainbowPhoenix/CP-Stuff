import win32gui
import win32con
import functools


class _WrapperFn:
    def __init__(self, fn, *message):
        self.message = message
        self.fn = fn

    def __call__(self, target, hwnd, message, wparam, lparam):
        if len(self.message) == 0 or (message in self.message):
            return self.fn(target, hwnd, message, wparam & 0xffffffff, lparam & 0xffffffff)


def subscribe(*message):
    def wrapper(fn):
        return _WrapperFn(fn, *message)

    if isinstance(message[0], int):
        return wrapper
    else:
        return _WrapperFn(message[0])


def subscriber(clz):
    class WndMessageSubscriber(clz):
        def __init__(self, *args, **kwargs):
            clz.__init__(self, *args, **kwargs)
            self.__bind_events = False
            self.subscriptions = []
            for key in dir(self):
                fn = self.__getattribute__(key)
                if isinstance(fn, _WrapperFn):
                    bound_fn = functools.partial(fn, self)
                    self.subscriptions.append(bound_fn)
            self.__bind_events = True

        def __getattribute__(self, name):
            v = clz.__getattribute__(self, name)
            if isinstance(v, _WrapperFn) and self.__bind_events:
                return functools.partial(v, self)
            else:
                return v

        def get_wnd_proc(self):
            def wnd_proc(*args):
                for fn in self.subscriptions:
                    if fn(*args):
                        break
                else:
                    win32gui.DefWindowProc(*args)

            return wnd_proc

    return WndMessageSubscriber
