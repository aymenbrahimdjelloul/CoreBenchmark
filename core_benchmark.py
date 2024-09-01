"""
@author : Aymen Brahim Djelloul
version : 1.0
date : 01.09.2024
License : MIT



"""

# IMPORTS
import sys
from time import perf_counter
from math import ceil
from decimal import Decimal, getcontext
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor, as_completed

# DEFINE BASIC VARIABLES
AUTHOR: str = "Aymen Brahim Djellou"
VERSION: float = 1.0
PI_PRECISION: int = 10000


class CoreBenchmark:

    def __init__(self) -> None:
        # Define variables
        self.cpu_cores: int = cpu_count()

    def benchmark(self, score_result: bool = True) -> float:
        """
        Benchmark method that calls the calculating pi method
        
        Args:
        - friendly_format: Boolean argument to return the right type of data
        
        Returns:
        - Float representing the benchmark time result
        """
        # Get the start time
        s_time: float = perf_counter()
        # Calculate Pi number
        pi: Decimal = self._calculate_pi()
        # Get the benchmark time
        t_time: float = perf_counter() - s_time

        # Clear memory
        del pi, s_time

        # Return benchmark result
        return self._calculate_score(t_time) if score_result else t_time

    def benchmark_all_cores(self, score_result: bool = True) -> float:
        """
        Calculate π in parallel using multiple cores.
        
        Args:
        - friendly_format: Boolean argument to return the right type of data

        Returns:
        - Time taken to calculate π
        """
        chunk_size: int = PI_PRECISION // self.cpu_cores
        futures: list = []
        results = [Decimal(0) for _ in range(self.cpu_cores)]

        s_time: float = perf_counter()

        with ProcessPoolExecutor() as executor:
            for i in range(self.cpu_cores):
                start: int = i * chunk_size
                end: int = start + chunk_size
                if i == self.cpu_cores - 1:  # Last chunk might need to handle the remainder
                    end = PI_PRECISION
                futures.append(executor.submit(self._calculate_pi, start, end))
            
            for i, future in enumerate(as_completed(futures)):
                results[i] = future.result()

        # Combine results - for Chudnovsky, accurate combination would require specific techniques
        pi: float = sum(results) / len(results)
        # Get the taken time
        t_time: float = perf_counter() - s_time

        # Clear memory
        del (chunk_size, futures,
              results, s_time, start, end, i, [pi])

        # Return the benchmark result
        return self._calculate_score(t_time) if score_result else t_time
    
    def _calculate_pi(self, start: int = 0, end: int = PI_PRECISION) -> Decimal:
        """
        Calculate a chunk of π using the Chudnovsky algorithm.
        
        Args:
        - start: The starting index for the chunk.
        - end: The ending index for the chunk.

        Returns:
        - A Decimal object representing π for the chunk.
        """
        getcontext().prec = PI_PRECISION + 2  # Set precision

        C = Decimal(426880) * Decimal(10005).sqrt()
        K = Decimal(6 + 12 * start)
        M = Decimal(1)
        X = Decimal(1)
        L = Decimal(13591409 + 545140134 * start)
        S = L

        for i in range(start + 1, end):
            M *= (K**3 - 16*K) / (i**3)
            L += Decimal(545140134)
            X *= -262537412640768000
            S += Decimal(M * L) / X
            K += 12

        # Return the pi number
        return C / S


    def _calculate_score(self, time_taken: float, scale: float = 10000.0, offset: float = 1.0) -> float:
        """
        Calculate a score based on the given duration in seconds.
        Lower durations result in higher scores, with customizable scaling and offset.

        Args:
            duration (float): The duration in seconds to calculate the score from.
            scale (float): A scaling factor to adjust the score range. Default is 100.
            offset (float): An offset to adjust the score range. Default is 1.

        Returns:
            float: The calculated score.
        """
        
        # Custom scoring formula
        return ceil(scale / (time_taken + offset))  # Adding offset to avoid division by zero
        

if __name__ == "__main__":
    sys.exit()
