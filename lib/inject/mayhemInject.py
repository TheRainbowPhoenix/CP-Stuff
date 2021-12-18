import sys
import ctypes.util

# Resolving python.dll path in order to inject it in the target process
from mayhem.proc import ProcessError

python_library = 'python{}{}.dll'.format(sys.version_info.major, sys.version_info.minor)
python_library = ctypes.util.find_library(python_library)

from mayhem import utilities
from mayhem.proc.windows import WindowsProcess
from mayhem.windll import kernel32

try:
    process = WindowsProcess(exe="C:\\Windows\\SysWOW64\\notepad.exe")
except ProcessError as error:
    print("[-] {0}".format(error.msg))
    sys.exit(1)

# Resolving Py_InitializeEx address in the remote process
python_library_remote = process.load_library(python_library)
python_library_local = kernel32.GetModuleHandleW(python_library)

initializer = python_library_remote + (
        kernel32.GetProcAddress(python_library_local, b'Py_InitializeEx') - python_library_local)

# Calling Py_InitializeEx(0) in the remote process
process.join_thread(process.start_thread(initializer, 0))


source_code = r"""
print("hello !")
"""

# PyRun_SimpleString uses utf-8 encoded strings
injected_code = source_code.encode('utf-8') + b'\x00'

# Allocate some memory in the remote process to place our Python code there
alloced_address = process.allocate(
    size=utilities.align_up(len(injected_code)), permissions='PAGE_READWRITE')

# Put utf-8 encoded Python source code into the allocated memory
process.write_memory(alloced_address, injected_code)

# Run PyRun_SimpleString in a new thread in the remote process
# process.start_thread(code_runner, alloced_address)

