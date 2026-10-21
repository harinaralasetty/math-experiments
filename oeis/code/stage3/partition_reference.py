"""Fix outer partitions; search for globally disjoint strict refinements."""
from functools import lru_cache

def partitions(n,low=1):
    if n==0:
        yield ()
        return
    for x in range(low,n+1):
        for tail in partitions(n-x,x):yield (x,)+tail

@lru_cache(None)
def refinements(n,low=1):
    if n==0:return (0,)
    return tuple((1<<x)|tail for x in range(low,n+1) for tail in refinements(n-x,x+1))

@lru_cache(maxsize=200000)
def possible(parts,used=0):
    if not parts:return True
    return any(mask&used==0 and possible(parts[1:],used|mask) for mask in refinements(parts[0]))

def count(n,no_ones):
    return sum(not possible(p) for p in partitions(n,2 if no_ones else 1))
