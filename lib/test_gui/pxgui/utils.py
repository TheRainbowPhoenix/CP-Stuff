from .common import winapiconsts as w32const

_MESSAGE_NAME = {}

for k in dir(w32const):
    v = w32const.__dict__.get(k)
    if isinstance(v, int) and k[:3] == 'WM_':
        _MESSAGE_NAME[v] = k


def get_message_name(message):
    return _MESSAGE_NAME[message] if message in _MESSAGE_NAME else ("UNKNOWN(0x%x)" % message)
