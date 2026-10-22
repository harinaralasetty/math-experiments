# (Python)

import collections, itertools, math

from functools import lru_cache

def term(n):
 counts=[0]*(n+1)
 def rec(left,first,last,length,diffs):
  if left==0:
   if first-last not in diffs:counts[length]+=1
   return
  for x in range(1,left+1):
   d=x-last
   if d not in diffs:rec(left-x,first,x,length+1,diffs|{d})
 for first in range(1,n+1):rec(n-first,first,first,1,set())
 assert all(v%k==0 for k,v in enumerate(counts) if k)
 return sum(v//k for k,v in enumerate(counts) if k)

def a(n):
    return term(n)
