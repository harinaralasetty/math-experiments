"""Definition-based Python implementations, with exact integers only."""
import collections,itertools,json,math,sys,time
from functools import lru_cache

def partitions(n,lo=1,strict=False):
 if n==0:yield ()
 for k in range(lo,n+1):
  for q in partitions(n-k,k+int(strict),strict):yield (k,)+q

def vertical(p):
 # Gale-Ryser criterion for a 0/1 matrix with both margins p.
 q=sorted(p,reverse=True)
 return all(sum(q[:k])<=sum(min(k,d) for d in q) for k in range(1,len(q)+1))

def split_count(p):
 def rec(i,used):
  if i==len(p):return 1
  out=s=0
  for j in range(i,len(p)):
   s+=p[j]
   if s not in used:out+=rec(j+1,used|{s})
  return out
 return rec(0,set())

def recursive_mult(p):
 if len(p)<=1:return True
 c=collections.Counter(p);m=tuple(sorted(c.values()));cm=collections.Counter(m)
 return all(c[k]>=v for k,v in cm.items()) and recursive_mult(m)

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

def normal_pred(p,a):
 if not p:return True
 if (a=='A332297' and len(p)==1) or (a!='A332297' and set(p)=={1}):return True
 if set(p)!=set(range(1,max(p)+1)):return False
 c=[len(list(g)) for _,g in itertools.groupby(p)]
 # p is descending.
 if a=='A332278':
  if c!=sorted(c):return False
 else:
  if c!=sorted(c,reverse=True):return False
 if a=='A332292':c=c[::-1]
 return normal_pred(tuple(c),a)

def normal_count(n,a):
 if not n:return 1
 out=int(a=='A332297' and n>1) # non-normal singletons
 # Generate normal partitions by assigning nonzero multiplicity to each 1..k.
 for k in range(1,math.isqrt(2*n)+1):
  if k*(k+1)//2>n:break
  def r(i,left,counts):
   if i>k:
    if left:return 0
    p=tuple(v for v,c in reversed(list(enumerate(counts,1))) for _ in range(c))
    return int(normal_pred(p,a))
   reserve=sum(range(i+1,k+1))
   return sum(r(i+1,left-i*c,counts+[c]) for c in range(1,(left-reserve)//i+1))
  out+=r(1,n,[])
 return out

def loopgraph(p):
 d=sorted(p,reverse=True)
 # Loopy graphical degree criterion, with every loop contributing two.
 return all(sum(d[:k])<=k*(k+1)+sum(min(k,x) for x in d[k:]) for k in range(1,len(d)+1))

def term(a,n):
 if a in ['A332278','A332292','A332297']:return normal_count(n,a)
 if a in ['A339655','A339656']:
  return sum(loopgraph(p)==(a=='A339656') for p in partitions(2*n))
 ps=partitions(n,strict=a=='A304382')
 if a in ['A321728','A321729']:return sum(vertical(p)==(a=='A321729') for p in ps)
 if a=='A336131':return sum(split_count(p) for p in ps)
 if a=='A353426':return sum(recursive_mult(p) for p in ps)
 if a=='A304382':return sum(ztree(p) for p in ps)
 if a in ['A320052','A320053','A320054']:
  return sum(knapsack(p,product_sum=a!='A320053',spanning=a!='A320052') for p in ps)
 raise ValueError(a)

if __name__=='__main__':
 a=sys.argv[1];first,last=map(int,sys.argv[2:4])
 for n in range(first,last+1):
  t=time.perf_counter();v=term(a,n)
  print(json.dumps(dict(n=n,value=v,seconds=time.perf_counter()-t)),flush=True)
