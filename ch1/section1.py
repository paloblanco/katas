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

# %%
