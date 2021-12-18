#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import ctypes
import ctypes.util
import os
import sys

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mayhem import utilities
from mayhem.datatypes import windows as wintypes
from mayhem.proc import ProcessError
from mayhem.proc.windows import WindowsProcess
from mayhem.windll import kernel32 as m_k32


class Injector:
    """Class that allows running arbitrary Python code in any process"""

    def initialize(self):
        """Calls Py_InitializeEx(0) in the remote process"""
        pass

    def finalize(self):
        """Calls Py_FinalizeEx(0) in the remote process"""
        pass

    def run_code(self, source_code, should_wait=False):
        """Runs the Python source code in the remote process in a separate thread"""
        pass
    
source_code = """
import ctypes
ctypes.windll.user32.MessageBoxA(0, b"Hello from Python", b"Hello from Python", 0)
"""

process = WindowsProcess(pid=11224)

python_lib = "python{0}{1}.dll".format(sys.version_info.major, sys.version_info.minor)
python_lib = ctypes.util.find_library(python_lib)

python_library_remote = process.load_library(python_lib)
python_library_local = m_k32.GetModuleHandleW(python_lib)

initializer = python_library_remote + (
        m_k32.GetProcAddress(python_library_local, b'Py_InitializeEx') - python_library_local)

code_runner = python_library_remote + (
        m_k32.GetProcAddress(python_library_local, b'PyRun_SimpleString') - python_library_local)

# Calling Py_InitializeEx(0) in the remote process
process.join_thread(process.start_thread(initializer, 0))

# PyRun_SimpleString uses utf-8 encoded strings
injected_code = source_code.encode('utf-8') + b'\x00'

# Allocate some memory in the remote process to place our Python code there
alloced_address = process.allocate(
    size=utilities.align_up(len(injected_code)), permissions='PAGE_READWRITE')

# Put utf-8 encoded Python source code into the allocated memory
process.write_memory(alloced_address, injected_code)

# Run PyRun_SimpleString in a new thread in the remote process
thread = process.start_thread(code_runner, alloced_address)

process.join_thread(thread)



# injector.run_code(code, should_wait=True)

