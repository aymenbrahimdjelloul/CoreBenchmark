"""
@author : Aymen Brahim Djelloul
version : 1.1
date : 01.09.2024
License : MIT


    CoreBenchmark is a streamlined and efficient tool designed to benchmark computational
    performance by calculating π (pi) to an accuracy of 10,000 decimal places. With its
    straightforward approach, CoreBenchmark provides an accurate measure of your system's
    processing power and precision capabilities. Ideal for performance testing and optimization, this tool
    leverages advanced algorithms to deliver reliable and comprehensive benchmarks.

"""

# IMPORTS
import sys
from decimal import Decimal, getcontext
from math import ceil
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Process, ProcessError, Queue
from time import perf_counter, sleep
from os import system
from cpuinfo import CPU

# DEFINE BASIC VARIABLES
AUTHOR: str = "Aymen Brahim Djelloul"
VERSION: float = 1.2
PI_PRECISION: int = 10000
CONSOLE_CLEAR_WIN32: str = "cls"
CONSOLE_CLEAR_LINUX: str = "clear"

# Create CPU object
cpu = CPU()


def is_executable():
    """ This function will detect if running on executable file or .py"""
    return True if sys.argv[0].endswith(".exe") else False


def clear_console():
    """ This function will clear the console for both windows and linux systems"""
    system(CONSOLE_CLEAR_WIN32 if sys.platform == "win32" else CONSOLE_CLEAR_LINUX)


def set_title():
    """ This function will set console title for Windows version only"""
    system(f"title CoreBenchmark {VERSION}v")


class CoreBenchmark:
    """
    CoreBenchmark is the main class to perform CPU computation performance tests.

    Methods
    -------
    benchmark() -> float
        This method runs a single-core benchmark.

    benchmark_all_cores() -> float
        This method runs a benchmark for all CPU cores in parallel.
    """

    def __init__(self) -> None:
        # Define variables
        self.cpu_cores: int = cpu.get_core_count()

    def benchmark(self, score_result: bool = True) -> float:
        """
        Benchmark method that calls the calculating pi method.

        Args:
        - score_result (bool): Return benchmark score if True, otherwise return raw time.

        Returns:
        - float: The benchmark score or time result.
        """
        # Get the start time
        s_time: float = perf_counter()
        # Calculate Pi number
        self._calculate_pi(end=PI_PRECISION)
        # Get the benchmark time
        t_time: float = perf_counter() - s_time

        return self._calculate_score(t_time) if score_result else t_time

    def benchmark_all_cores(self, score_result: bool = True) -> float:
        """
        Calculate π in parallel using multiple cores.

        Args:
        - score_result (bool): Return benchmark score if True, otherwise return raw time.

        Returns:
        - float: Time taken to calculate π or the score result.
        """
        chunk_size: int = PI_PRECISION // self.cpu_cores
        futures = []
        results = [Decimal(0) for _ in range(self.cpu_cores)]

        s_time: float = perf_counter()

        with ProcessPoolExecutor() as executor:
            for i in range(self.cpu_cores):
                start: int = i * chunk_size
                end: int = start + chunk_size
                if i == self.cpu_cores - 1:  # Handle remainder in the last chunk
                    end = PI_PRECISION
                futures.append(executor.submit(self._calculate_pi, end, start))

            for i, future in enumerate(as_completed(futures)):
                results[i] = future.result()

        # Combine results (for Chudnovsky, specific combination may be needed)
        pi: Decimal = sum(results)
        t_time: float = perf_counter() - s_time

        return self._calculate_score(t_time) if score_result else t_time

    @staticmethod
    def _calculate_pi(end: int, start: int = 0) -> Decimal:
        """
        Calculate a chunk of π using the Chudnovsky algorithm.

        Args:
        - start (int): The starting index for the chunk.
        - end (int): The ending index for the chunk.

        Returns:
        - Decimal: The calculated value of π for the chunk.
        """
        getcontext().prec = PI_PRECISION + 2  # Set precision

        c = Decimal(426880) * Decimal(10005).sqrt()
        k = Decimal(6 + 12 * start)
        m = Decimal(1)
        x = Decimal(1)
        l = Decimal(13591409 + 545140134 * start)
        s = l

        for i in range(start + 1, end):
            m *= (k ** 3 - 16 * k) / (i ** 3)
            l += Decimal(545140134)
            x *= -262537412640768000
            s += Decimal(m * l) / x
            k += 12

        # Return the pi number for the chunk
        return c / s

    @staticmethod
    def _calculate_score(time_taken: float, scale: float = 10000.0, offset: float = 1.0) -> float:
        """
        Calculate a score based on the given time duration.

        Args:
        - time_taken (float): The time taken for the benchmark in seconds.
        - scale (float): A scaling factor to adjust the score range.
        - offset (float): An offset to avoid division by zero.

        Returns:
        - float: The calculated score.
        """
        return ceil(scale / (time_taken + offset))  # Adding offset to avoid division by zero


def main():

    # Create CoreBenchmark object
    bench = CoreBenchmark()

    # Print CoreBenchmark banner
    print(
        f"\n       CoreBenchmark {VERSION}v   |   Developed by {AUTHOR}\n\n"
        f"     Multi-core Benchmark running on [ {cpu.get_cpu_name()} ]\n"
        "      Please wait...\n"
    )

    try:
        # Check if CoreBenchmark running on windows on executable file '.exe'

        if is_executable():
            # Set console title
            set_title()

            # Print out Note that the results on the executable version may not be accurate
            print(f"\n     NOTE: Results may not be accurate with the executable version.\n"
                  f"     look : https://github.com/aymenbrahimdjelloul/CoreBenchmark")

            # Run benchmark process
            bench_score: int = bench.benchmark()
            # Print out the results multiplied by the cores number
            print(f"\n\n     Benchmark score : {bench_score * bench.cpu_cores} points\n")

        else:

            # Run the normal multicore benchmark
            bench_score: int = bench.benchmark_all_cores()
            print(f"\n     Benchmark score : {bench_score} points\n")

    # Handle exceptions
    except Exception as e:
        print(f"    {e}")

    # Wait user input to retry or exit
    i: int = input("\nENTER [1] For retry .. [2] For exit\n>>: ")

    match int(i):
        case 1:
            # Clear console
            clear_console()
            # Rerun CoreCheck
            main()

        case 2:
            sys.exit()

        case _:
            print(f"    CoreBenchmark Exiting right now ..")
            sleep(2)
            sys.exit()


if __name__ == "__main__":
    main()
