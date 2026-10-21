"""Exact Python reference algorithms. No term is requested beyond the cached listing."""
from collections import deque
from functools import lru_cache
from math import isqrt

def digit_multiple(n):
    # Count is capped at n: 'containing n eights' means at least n.
    queue = deque()
    parent = {}
    for d in range(1, 10):
        state = (d % n, int(d == 8))
        if state not in parent:
            parent[state] = (None, str(d))
            queue.append(state)
    while queue:
        state = queue.popleft()
        r, c = state
        if r == 0 and c == n:
            out = ''
            while state is not None:
                state, d = parent[state]
                out = d + out
            return int(out)
        for d in range(10):
            nxt = ((10*r+d) % n, min(n, c+(d == 8)))
            if nxt not in parent:
                parent[nxt] = (state, str(d))
                queue.append(nxt)
    raise AssertionError('unreachable')

def primes_to(limit):
    sieve = bytearray(b'\1') * (limit+1)
    if limit >= 0: sieve[0] = 0
    if limit >= 1: sieve[1] = 0
    for p in range(2, isqrt(limit)+1):
        if sieve[p]:
            sieve[p*p::p] = b'\0' * ((limit-p*p)//p+1)
    return [p for p in range(2, limit+1) if sieve[p]]

def prime_minima(n, bound):
    # A factor p^1 contributes zero and can be removed from any minimizer.
    # Thus every contributing prime is <= sqrt(bound). Multiple-choice
    # multiplicative knapsack processes each prime exactly once.
    dp = [1] + [bound+1] * n
    for p in primes_to(isqrt(bound)):
        old = dp[:]
        power, exponent = p*p, 2
        while power <= bound:
            score = p % exponent
            if 0 < score <= n:
                for s in range(n-score+1):
                    value = old[s]*power
                    if value < dp[s+score]:
                        dp[s+score] = value
            power *= p
            exponent += 1
    if max(dp) > bound:
        raise ValueError('cap does not enclose all required minima')
    return dp

def partitions(n, minimum=1):
    if not n:
        yield ()
    for p in range(minimum, n+1):
        for tail in partitions(n-p, p):
            yield (p,) + tail

@lru_cache(None)
def strict_masks(n, minimum=1):
    if n == 0:
        return (0,)
    return tuple((1 << p) | tail
        for p in range(minimum, n+1)
        for tail in strict_masks(n-p, p+1))

@lru_cache(None)
def feasible(parts, used=0):
    if not parts:
        return True
    return any(not (mask & used) and feasible(parts[1:], used | mask)
        for mask in strict_masks(parts[0]))

def partition_count(n, no_ones=False, complement=False):
    return sum(feasible(p) != complement
        for p in partitions(n, 2 if no_ones else 1))

PARTITION_OPTIONS = {
    'A383708': (False, False), 'A383710': (False, True),
    'A383533': (True, False), 'A383711': (True, True),
}
