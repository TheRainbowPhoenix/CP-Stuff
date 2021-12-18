#!/bin/env python
# -*- coding: utf-8 -*-

from winappdbg import Debug, EventHandler
from winappdbg.win32 import *  # NOQA
from ctypes.wintypes import *

class MyEventHandler(EventHandler):
    # Here we set which API calls we want to intercept.
    apiHooks = {
        # Hooks for the kernel32 library.
        'kernel32.dll': [

            #  Function            Parameters
            ('CreateFileA', (PVOID, DWORD, DWORD, PVOID, DWORD, DWORD, HANDLE)),
            ('CreateFileW', (PVOID, DWORD, DWORD, PVOID, DWORD, DWORD, HANDLE)),
            ('LoadLibraryW', tuple([LPCWSTR])),
            ('LoadLibraryExW', (LPCWSTR, HANDLE, DWORD)),
            ('GetFileAttributesW', tuple([PVOID])),
            ('GetFileAttributesA', tuple([PVOID])),

        ],

        'KernelBase.dll': [
            ('ReadFile', (HANDLE, LPVOID, DWORD, LPDWORD, LPOVERLAPPED)),
        ],

        # Hooks for the advapi32 library.
        'advapi32.dll': [

            #  Function            Parameters
            ('RegCreateKeyExA', (HKEY, PVOID, DWORD, PVOID, DWORD, REGSAM, PVOID, PVOID, PVOID)),
            ('RegCreateKeyExW', (HKEY, PVOID, DWORD, PVOID, DWORD, REGSAM, PVOID, PVOID, PVOID)),
        ],
    }


def simple_debugger(argv):
    # Instance a Debug object, passing it the MyEventHandler instance.
    with Debug(MyEventHandler(), bKillOnExit=True) as debug:
        # Start a new process for debugging.
        debug.execv(argv)

        # Wait for the debugee to finish.
        debug.loop()


if __name__ == "__main__":
    import sys

    simple_debugger(sys.argv[1:])
