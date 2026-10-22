# (Python)

import collections, itertools, math

from functools import lru_cache

def partitions(n,lo=1,strict=False):
 if n==0:yield ()
 for k in range(lo,n+1):
  for q in partitions(n-k,k+int(strict),strict):yield (k,)+q

def split_count(p):
 def rec(i,used):
  if i==len(p):return 1
  out=s=0
  for j in range(i,len(p)):
   s+=p[j]
   if s not in used:out+=rec(j+1,used|{s})
  return out
 return rec(0,set())

def a(n):
    return sum(split_count(p) for p in partitions(n))
