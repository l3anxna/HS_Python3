import multiprocessing
from math import factorial
from decimal import Decimal, getcontext
import time

def e_serie_part(start, end):
    """Calculate a part of the series for e."""
    e_part = Decimal(0)
    for i in range(start, end):
        e_part += Decimal(1) / Decimal(factorial(i))
    return e_part

def main():
    getcontext().prec = 100
    
    N = 10000
    processes_count = multiprocessing.cpu_count()

    print(f"Number of cores: {processes_count}")

    start_time = time.time()

    with multiprocessing.Pool(processes=processes_count) as pool:
        ranges = [(N * i, N * (i + 1)) for i in range(processes_count)]
        
        results = pool.starmap(e_serie_part, ranges)

    end_time = time.time()

    print(f"Processes finished. Elapsed time: {end_time - start_time} seconds.")

    e_approx = sum(results)

    print(f"Approximation of e: {e_approx}")

if __name__ == "__main__":
    main()