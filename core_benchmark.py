"""
@author : Aymen Brahim Djelloul
version : 1.3
date : 14.04.2025
License : MIT

CoreBenchmark: CoreBenchmark is a streamlined and efficient tool designed to benchmark
 computational performance by calculating π (pi) to an accuracy of 10,000 decimal places.
  With its straightforward approach, CoreBenchmark provides an accurate measure of your system's
   processing power and precision capabilities. Ideal for performance testing and optimization,
    this tool leverages advanced algorithms to deliver reliable and comprehensive benchmarks.

    look : https://github.com/aymenbrahimdjelloul/CoreBenchmark
"""

# IMPORTS
import sys
import ctypes
import colorama
from math import ceil
from os import system
from ctypes import wintypes
from colorama import Fore, Style
from decimal import Decimal, getcontext
from concurrent.futures import ProcessPoolExecutor, as_completed
from time import perf_counter, sleep

# Initialize colorama for cross-platform colored output
colorama.init(autoreset=True)

# Constants
VERSION: float = 1.3
TITLE: str = f"CoreBenchmark - V {VERSION}"
PI_PRECISION: int = 10000


def is_executable():
    """Detects if running from an executable."""
    return sys.argv[0].endswith(".exe")


def clear_console():
    """Clears the console."""
    system("cls" if sys.platform == "win32" else "clear")


def set_console_title():
    """Sets the console title."""
    system(f"title {TITLE}" if sys.platform == "win32" else f'echo -ne "\\033]0;{TITLE}\\007"')


class Processor:
    """Handles CPU information retrieval."""

    @staticmethod
    def get_cpu_name():
        """Retrieves the CPU name."""
        if sys.platform == "win32":
            try:
                advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
                reg_open_key_ex = advapi32.RegOpenKeyExW
                reg_query_value_ex = advapi32.RegQueryValueExW
                reg_close_key = advapi32.RegCloseKey

                hkey = wintypes.HKEY()
                result = ctypes.create_unicode_buffer(256)
                data_size = wintypes.DWORD(256)

                if (
                    reg_open_key_ex(
                        0x80000002,
                        r"HARDWARE\DESCRIPTION\System\CentralProcessor\0",
                        0,
                        0x20019,
                        ctypes.byref(hkey),
                    )
                    != 0
                ):
                    return "Unknown CPU"

                if (
                    reg_query_value_ex(
                        hkey,
                        "ProcessorNameString",
                        None,
                        None,
                        ctypes.byref(result),
                        ctypes.byref(data_size),
                    )
                    != 0
                ):
                    return "Unknown CPU"

                reg_close_key(hkey)
                return result.value.strip()

            except Exception:
                return "Unknown CPU"

        elif sys.platform == "linux":
            try:
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if line.startswith("model name"):
                            return line.split(":")[1].strip()
            except Exception:
                return "Unknown CPU"

        else:
            return "Unsupported OS"

    @staticmethod
    def get_core_count():
        """Retrieves the number of CPU cores."""
        if sys.platform == "win32":
            try:
                kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
                sys_info = wintypes.SYSTEM_INFO()
                kernel32.GetSystemInfo(ctypes.byref(sys_info))
                return sys_info.dwNumberOfProcessors
            except Exception:
                return -1
        elif sys.platform == "linux":
            try:
                import subprocess

                return int(subprocess.check_output(["nproc"]).decode().strip())
            except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
                return 0
        else:
            return -1


class CoreBenchmark:
    """Performs CPU performance benchmarks."""

    def __init__(self):
        self.cpu_cores = Processor.get_core_count()

    def benchmark(self, score_result=True):
        """Single-core benchmark."""
        start_time = perf_counter()
        self._calculate_pi(end=PI_PRECISION)
        time_taken = perf_counter() - start_time
        return self._calculate_score(time_taken) if score_result else time_taken

    def benchmark_all_cores(self, score_result=True):
        """Multi-core benchmark."""
        chunk_size = PI_PRECISION // self.cpu_cores
        futures = []
        results = [Decimal(0) for _ in range(self.cpu_cores)]

        start_time = perf_counter()

        with ProcessPoolExecutor() as executor:
            for i in range(self.cpu_cores):
                start = i * chunk_size
                end = start + chunk_size
                if i == self.cpu_cores - 1:
                    end = PI_PRECISION
                futures.append(executor.submit(self._calculate_pi, end, start))

            for i, future in enumerate(as_completed(futures)):
                results[i] = future.result()
                print("work")

        time_taken = perf_counter() - start_time
        return self._calculate_score(time_taken) if score_result else time_taken

    @staticmethod
    def _calculate_pi(end, start=0):
        """Calculates π using the Chudnovsky algorithm."""
        getcontext().prec = PI_PRECISION + 2

        c = Decimal(426880) * Decimal(10005).sqrt()
        k = Decimal(6 + 12 * start)
        m = Decimal(1)
        x = Decimal(1)
        l = Decimal(13591409 + 545140134 * start)
        s = l

        for i in range(start + 1, end):
            m *= (k**3 - 16 * k) / (i**3)
            l += Decimal(545140134)
            x *= -262537412640768000
            s += Decimal(m * l) / x
            k += 12

        return c / s

    @staticmethod
    def _calculate_score(time_taken, scale=10000.0, offset=1.0):
        """Calculates a benchmark score."""
        return ceil(scale / (time_taken + offset))


def main():
    """Main function."""

    # Create Processor object
    cpu = Processor()
    # Create CoreBenchmark object
    bench = CoreBenchmark()

    # Set console title
    set_console_title()

    print(f"\n  {Fore.MAGENTA}   CoreBenchmark {VERSION}v   |   Developed by Aymen Brahim Djelloul\n\n"
          f"     Multi-core Benchmark running on [ {cpu.get_cpu_name()} ]\n"
          f"    {Fore.YELLOW}{Style.NORMAL}Please Wait..")

    try:

        score = bench.benchmark_all_cores()
        print(f"\n  {Fore.GREEN}{Style.BRIGHT}Benchmark score : {score} points\n\n\n\n")

    except Exception as e:
        print(f" ERROR : CoreBenchmark cannot run ! \n {e}")

    choice = input("\n\nENTER [1] For retry .. [2] For exit\n\n>>: ")

    if choice == "1":
        clear_console()
        main()

    elif choice == "2":
        sys.exit()

    else:
        print("    CoreBenchmark Exiting right now ..")
        sleep(2)
        sys.exit()


if __name__ == "__main__":
    main()
