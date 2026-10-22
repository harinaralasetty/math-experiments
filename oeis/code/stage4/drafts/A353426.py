# (Python)

import collections, itertools, math

from functools import lru_cache

def partitions(n,lo=1,strict=False):
 if n==0:yield ()
 for k in range(lo,n+1):
  for q in partitions(n-k,k+int(strict),strict):yield (k,)+q

def recursive_mult(p):
 if len(p)<=1:return True
 c=collections.Counter(p);m=tuple(sorted(c.values()));cm=collections.Counter(m)
 return all(c[k]>=v for k,v in cm.items()) and recursive_mult(m)

def a(n):
    return sum(recursive_mult(p) for p in partitions(n))
