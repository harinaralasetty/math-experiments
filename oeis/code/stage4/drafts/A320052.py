# (Python)

import collections, itertools, math

from functools import lru_cache

def partitions(n,lo=1,strict=False):
 if n==0:yield ()
 for k in range(lo,n+1):
  for q in partitions(n-k,k+int(strict),strict):yield (k,)+q

@lru_cache(None)
def multiset_partitions(p):
 if not p:return ((),)
 v=p[-1];out=set()
 for b in multiset_partitions(p[:-1]):
  out.add(tuple(sorted(b+((v,),))))
  for i in range(len(b)):
   out.add(tuple(sorted(b[:i]+b[i+1:]+(tuple(sorted(b[i]+(v,))),))))
 return tuple(out)

def submultisets(p):
 c=collections.Counter(p)
 for cs in itertools.product(*(range(v+1) for v in c.values())):
  yield tuple(x for (x,_),k in zip(c.items(),cs) for _ in range(k))

def knapsack(p,product_sum=True,spanning=False):
 if product_sum and not spanning and 1 in p:return False
 seen=set()
 for q in ([p] if spanning else submultisets(p)):
  for b in multiset_partitions(q):
   v=math.prod(map(sum,b)) if product_sum else sum(map(math.prod,b))
   if v in seen:return False
   seen.add(v)
 return True

def a(n):
    return sum(knapsack(p) for p in partitions(n))
