#%%

def fib1(n: int) -> int:
    return fib1(n-1) + fib1(n-2)


#%%

def fib2(n: int) -> int:
    if n < 2:
        return n
    return fib2(n-2) + fib2(n-1)

#%%
from typing import Dict
memo: Dict[int, int] = {0:0,1:1}

def fib3(n: int) -> int:
    if n not in memo:
        memo[n] = fib3(n-2) + fib3(n-1)
    return memo[n]

#%%
from functools import lru_cache

@lru_cache(maxsize=None)
def fib4(n: int) -> int:
    if n < 2:
        return n
    return fib4(n-2) + fib4(n-1)

print(fib3(50))
print(fib4(50))




# %%
def fib5(n: int) -> int:
    if n == 0: return 0
    last: int = 0
    next: int = 1
    for _ in range(1,n):
        last, next = next, next + last
    return next

fib5(1)

# %%
from typing import Generator

def fib6(n: int) -> Generator[int, None, None]:
    yield 0  # special case
    if n > 0: yield 1  # special case
    last: int = 0  # initially set to fib(0)
    next: int = 1  # initially set to fib(1)
    for _ in range(1, n):
        last, next = next, last + next
        yield next  # main generation step

for i in fib6(10):
    print(i)


def fib7(n: int) -> int:
    fib_value: int = 0
    fib_next: int = 1
    current_n: int = 0
    while current_n < n:
        fib_value, fib_next, current_n = fib_next, fib_value + fib_next, current_n+1
    return fib_value
        

def test_fib7():
    answer_10 = 55
    assert fib7(10) == answer_10

import timeit

def benchmark_fibs():

    
    f2 = timeit.timeit(stmt="fib2(10)",setup="from __main__ import fib2", number=100)
    f3 = timeit.timeit(stmt="fib3(10)",setup="from __main__ import fib3", number=100)
    f4 = timeit.timeit(stmt="fib4(10)",setup="from __main__ import fib4", number=100)
    f5 = timeit.timeit(stmt="fib5(10)",setup="from __main__ import fib5", number=100)
    f6 = timeit.timeit(stmt="fib6(10)",setup="from __main__ import fib6", number=100)
    f7 = timeit.timeit(stmt="fib7(10)",setup="from __main__ import fib7", number=100)
    
    print(f"Fib2: {str(f2)[:8]}")
    print(f"Fib3: {str(f3)[:8]}")
    print(f"Fib4: {str(f4)[:8]}")
    print(f"Fib5: {str(f5)[:8]}")
    print(f"Fib6: {str(f6)[:8]}")
    print(f"Fib7: {str(f7)[:8]}")

if __name__ == "__main__":
    test_fib7()
    benchmark_fibs()

# %%
