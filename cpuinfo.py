"""
@author : Aymen Brahim Djelloul
@version : 1.1
@date : 02.09.2024
@license : MIT
"""

# IMPORTS
import sys
import ctypes
from ctypes import wintypes


# PLATFORM-SPECIFIC IMPLEMENTATIONS
# WINDOWS CODE SECTION
if sys.platform == 'win32':

    # Load the kernel32 DLL for Windows system calls
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

    class CPU(ctypes.Structure):
        _fields_ = [
            ("wProcessorArchitecture", wintypes.WORD),
            ("wReserved", wintypes.WORD),
            ("dwPageSize", wintypes.DWORD),
            ("lpMinimumApplicationAddress", wintypes.LPVOID),
            ("lpMaximumApplicationAddress", wintypes.LPVOID),
            ("dwActiveProcessorMask", wintypes.LPVOID),
            ("dwNumberOfProcessors", wintypes.DWORD),
            ("dwProcessorType", wintypes.DWORD),
            ("dwAllocationGranularity", wintypes.DWORD),
            ("wProcessorLevel", wintypes.WORD),
            ("wProcessorRevision", wintypes.WORD),
        ]

        @staticmethod
        def get_cpu_name() -> str:
            """Returns the CPU name for Windows."""
            # try:
            #     # Query CPU name using WMIC
            #     return subprocess.check_output("wmic cpu get name", shell=True).decode().split('\n')[1].strip()
            # except subprocess.SubprocessError:
            #     return "Unknown CPU"

            try:
                HKEY_LOCAL_MACHINE = 0x80000002  # HKEY_LOCAL_MACHINE constant
                key_path = r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
                value_name = "ProcessorNameString"

                # Define types
                advapi32 = ctypes.WinDLL('advapi32', use_last_error=True)
                RegOpenKeyEx = advapi32.RegOpenKeyExW
                RegQueryValueEx = advapi32.RegQueryValueExW
                RegCloseKey = advapi32.RegCloseKey

                hkey = wintypes.HKEY()
                result = ctypes.create_unicode_buffer(256)  # Buffer to store CPU name
                data_size = wintypes.DWORD(256)  # Size of the buffer

                # Open registry key
                if RegOpenKeyEx(HKEY_LOCAL_MACHINE, key_path, 0, 0x20019, ctypes.byref(hkey)) != 0:
                    return "Unknown CPU"

                # Query CPU name from the registry
                if RegQueryValueEx(hkey, value_name, None, None, ctypes.byref(result), ctypes.byref(data_size)) != 0:
                    return "Unknown CPU"

                # Close the registry key
                RegCloseKey(hkey)

            # Errors handling
            except Exception as e:
                print(e)
                return None

            return result.value.strip()

        def get_core_count(self) -> int:
            """Returns the number of CPU cores for Windows."""
            try:
                kernel32.GetSystemInfo(ctypes.byref(self))
                return self.dwNumberOfProcessors

            except Exception as e:
                # Print out the occurring error
                print(e)
                return -1

# LINUX SYSTEMS CODE SECTION
elif sys.platform == 'linux':

    # IMPORTS
    import subprocess

    class CPU:

        @staticmethod
        def get_cpu_name() -> str:
            """Returns the CPU name for Linux."""
            try:
                # Efficiently retrieve CPU model from /proc/cpuinfo
                with open('/proc/cpuinfo', 'r') as f:
                    for line in f:
                        if line.startswith('model name'):
                            return line.split(':')[1].strip()
            except Exception:
                return "Unknown CPU"

        @staticmethod
        def get_core_count() -> int:
            """Returns the number of CPU cores for Linux."""
            try:
                # Use nproc to get core count efficiently
                return int(subprocess.check_output("nproc", shell=True).strip())
            except subprocess.SubprocessError:
                return 0


if __name__ == "__main__":
    sys.exit()
