from math import factorial
from decimal import Decimal, getcontext
import time

def e_serie(N):
    e_approx = Decimal(0)
    for i in range(N):
        e_approx += Decimal(1) / Decimal(factorial(i))
    return e_approx

def main():

    getcontext().prec = 100
    
    N = 1000

    start_time = time.time()
    

    e_approx = e_serie(N)

    end_time = time.time()

    print(f"Single-core calculation finished. Elapsed time: {end_time - start_time} seconds.")
    print(f"Approximation of e: {e_approx}")

if __name__ == "__main__":
    main()