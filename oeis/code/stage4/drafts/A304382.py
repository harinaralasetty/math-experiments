# (Python)

import collections, itertools, math

from functools import lru_cache

def partitions(n,lo=1,strict=False):
 if n==0:yield ()
 for k in range(lo,n+1):
  for q in partitions(n-k,k+int(strict),strict):yield (k,)+q

@lru_cache(None)
def prime_support(n):
 out=[];d=2
 while d*d<=n:
  if n%d==0:
   out.append(d)
   while n%d==0:n//=d
  d+=1
 if n>1:out.append(n)
 return frozenset(out)

def ztree(p):
 if len(p)==1:return True
 if any(b%a==0 for a,b in itertools.combinations(p,2)):return False
 supports=[prime_support(x) for x in p]
 if sum(len(s)-1 for s in supports)-len(set().union(*supports))!=-1:return False
 reached={0}
 while True:
  more={j for i in reached for j in range(len(p)) if math.gcd(p[i],p[j])>1}
  nxt=reached|more
  if nxt==reached:break
  reached=nxt
 return len(reached)==len(p)

def a(n):
    return sum(ztree(p) for p in partitions(n, strict=True))
