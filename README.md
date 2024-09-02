<!-- GitHub README.md -->

<h1 align="center">CoreBenchmark</h1>

<div>
  <a href="https://github.com/aymenbrahimdjelloul/CoreBenchmark/releases/download/v1.2/CoreBenchmark-1.2.exe">
    <img src="https://img.shields.io/badge/Download-CoreBenchmark-brightgreen" alt="Download">
  </a>
</div>

<p>  CoreBenchmark is a streamlined and efficient tool designed to benchmark computational performance by calculating π (pi) to an accuracy of 10,000 decimal places. With its straightforward approach, CoreBenchmark provides an accurate measure of your system's processing power and precision capabilities. Ideal for performance testing and optimization, this tool leverages advanced algorithms to deliver reliable and comprehensive benchmarks.

</p>

<h2>Features</h2>

- [x] Cross platform (CoreBenchmark support both of Windows and Linux systems)

- [x] Available with Simple & straight-forward Interface

- [x] Easy & Fast !

- [x] Pure python (No need for external dependencies)

<h2>How It's Work ?</h2>
<p1>
</p1>

<h2>Testing</h2>
<h4>CoreBenchmark results </h4>

| CPU  | Score|
|------|--------|
| AMD Ryzen 3 3200G | 940 |
| Intel Core i7-7600U 2.80 GHz | 800 |
| Intel Core i5-7Y54 1.20 Ghz | 600 |

Single core benchmark
-----
~~~python
from core_benchmark import CoreBenchmark

# Create CoreBenchmark object
bench = CoreBenchmark()

# Print the current cpu score
# on single core benchmark
print(bench.benchmark())


~~~

Multi-core benchmark
-----
~~~python
from core_benchmark import CoreBenchmark

# Create CoreBenchmark object
bench = CoreBenchmark()

# Print the current cpu score
# on Multi-core benchmark
print(bench.benchmark_all_cores())

~~~

<h2>License</h2>
<h4>This project is published under MIT License </h4>

~~~
MIT License

Copyright (c) 2023 Aymen Brahim Djelloul

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

~~~
