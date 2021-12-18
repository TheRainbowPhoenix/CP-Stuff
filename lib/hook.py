d#!/bin/env python
# -*- coding: utf-8 -*-

from winappdbg import Debug, EventHandler
from winappdbg.win32 import *  # NOQA
from ctypes.wintypes import *

SECURITY_INFORMATION = DWORD
PSECURITY_DESCRIPTOR = PVOID

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

            ('GetFileSecurityA', (LPCSTR, SECURITY_INFORMATION , PSECURITY_DESCRIPTOR , DWORD, LPDWORD)),

        ],
        'LanguageResource.dll': [
            ('InitLanguageResource', tuple([PVOID])),
            ('GetLangMessage', (UINT_PTR, LPWSTR))
        ]
    }

    # Now we can simply define a method for each hooked API.
    # Methods beginning with "pre_" are called when entering the API,
    # and methods beginning with "post_" when returning from the API.

    def pre_GetFileAttributesW(self, event, ra, lpFileName):
        self.__print_opening_ansi(event, "GetFileAttributesW", lpFileName)

    def pre_GetFileAttributesA(self, event, ra, lpFileName):
        self.__print_opening_ansi(event, "GetFileAttributesA", lpFileName)

    def pre_CreateFileA(self, event, ra, lpFileName, dwDesiredAccess,
                        dwShareMode, lpSecurityAttributes, dwCreationDisposition,
                        dwFlagsAndAttributes, hTemplateFile):

        self.__print_opening_ansi(event, "file", lpFileName)

    def pre_CreateFileW(self, event, ra, lpFileName, dwDesiredAccess,
                        dwShareMode, lpSecurityAttributes, dwCreationDisposition,
                        dwFlagsAndAttributes, hTemplateFile):

        self.__print_opening_unicode(event, "file", lpFileName)

    def pre_ReadFile(self, event, ra, hFile, lpBuffer, nNumberOfBytesToRead, lpNumberOfBytesRead, lpOverlapped):
        self.__print_reading(event, "file", hFile)

    def pre_RegCreateKeyExA(self, event, ra, hKey, lpSubKey, Reserved,
                            lpClass, dwOptions, samDesired,
                            lpSecurityAttributes, phkResult,
                            lpdwDisposition):

        self.__print_opening_ansi(event, "key", lpSubKey)

    def pre_RegCreateKeyExW(self, event, ra, hKey, lpSubKey, Reserved,
                            lpClass, dwOptions, samDesired,
                            lpSecurityAttributes, phkResult,
                            lpdwDisposition):

        self.__print_opening_unicode(event, "key", lpSubKey)

    def pre_GetFileSecurityA(self, lpFileName, RequestedInformation, pSecurityDescriptor, nLength, lpnLengthNeeded):
        print(f"GetFileSecurityA: {lpFileName}, {RequestedInformation}")

    def pre_InitLanguageResource(self):
        print("InitLanguageResource")

    def pre_GetLangMessage(self, num, msg):
        print(f"{num} {msg}")

    def pre_LoadLibraryW(self, lpLibFileName):
        print(f"LoadLibraryW {lpLibFileName}")

    def pre_LoadLibraryExW(self, lpLibFileName, hFile, dwFlags):
        print(f"LoadLibraryExW {lpLibFileName} {hFile} {dwFlags}")

    ## POST

    def post_CreateFileA(self, event, retval):
        self.__print_success(event, retval)

    def post_CreateFileW(self, event, retval):
        self.__print_success(event, retval)

    def post_ReadFile(self, event, ra, hFile, lpBuffer, nNumberOfBytesToRead, lpNumberOfBytesRead, lpOverlapped):
        self.__print_reading(event, "file", hFile)

    def post_RegCreateKeyExA(self, event, retval):
        self.__print_reg_success(event, retval)

    def post_RegCreateKeyExW(self, event, retval):
        self.__print_reg_success(event, retval)

    # Some helper private methods...

    def __print_reading(self, event, tag, pointer):
        # string = event.get_process().peek_string(pointer)
        tid = event.get_tid()
        print("%d: Reading %s: %s" % (tid, tag, "string"))

    def __print_opening_ansi(self, event, tag, pointer):
        string = event.get_process().peek_string(pointer)
        tid = event.get_tid()
        print("%d: Opening %s: %s" % (tid, tag, string))

    def __print_opening_unicode(self, event, tag, pointer):
        string = event.get_process().peek_string(pointer, fUnicode=True)
        tid = event.get_tid()
        print("%d: Opening %s: %s" % (tid, tag, string))

    def __print_success(self, event, retval):
        tid = event.get_tid()
        if retval:
            print("%d: Success: %x" % (tid, retval))
        else:
            print("%d: Failed!" % tid)

    def __print_reg_success(self, event, retval):
        tid = event.get_tid()
        if retval:
            print("%d: Failed! Error code: %x" % (tid, retval))
        else:
            print("%d: Success!" % tid)


def simple_debugger(argv):
    # Instance a Debug object, passing it the MyEventHandler instance.
    with Debug(MyEventHandler(), bKillOnExit=True) as debug:
        # Start a new process for debugging.
        debug.execv(argv)

        # Wait for the debugee to finish.
        debug.loop()


# When invoked from the command line,
# the first argument is an executable file,
# and the remaining arguments are passed to the newly created process.
if __name__ == "__main__":
    import sys

    simple_debugger(sys.argv[1:])
