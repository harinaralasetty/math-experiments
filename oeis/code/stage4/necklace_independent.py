"""Count rooted compositions by length, then divide by the free rotation action.
Distinct circular differences imply no nontrivial period when length > 1.
No lexicographic representative is constructed.
"""
import json,sys,time

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
if __name__=='__main__':
 for n in range(int(sys.argv[1]),int(sys.argv[2])+1):
  t=time.perf_counter();v=term(n);print(json.dumps(dict(n=n,value=v,seconds=time.perf_counter()-t)),flush=True)
