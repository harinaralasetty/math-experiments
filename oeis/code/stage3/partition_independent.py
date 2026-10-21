"""Enumerate globally distinct summands, partition them into unlabeled blocks."""
def strict(total,largest=None):
    if total==0:
        yield ()
        return
    for x in range(min(total,total if largest is None else largest),0,-1):
        for tail in strict(total-x,x-1):yield (x,)+tail

def total_partitions(n):
    # Euler's pentagonal recurrence, independent of the outer generator.
    p=[1]+[0]*n
    for m in range(1,n+1):
        k=1
        while k*(3*k-1)//2<=m:
            sign=1 if k%2 else -1
            p[m]+=sign*p[m-k*(3*k-1)//2]
            if k*(3*k+1)//2<=m:p[m]+=sign*p[m-k*(3*k+1)//2]
            k+=1
    return p

def count(n,no_ones):
    seen=set()
    for summands in strict(n):
        blocks=[]
        def visit(i):
            if i==len(summands):
                if not no_ones or 1 not in blocks:seen.add(tuple(sorted(blocks)))
                return
            x=summands[i]
            for j in range(len(blocks)):
                blocks[j]+=x;visit(i+1);blocks[j]-=x
            blocks.append(x);visit(i+1);blocks.pop()
        visit(0)
    p=total_partitions(n)
    total=p[n]-(p[n-1] if no_ones and n else 0)
    return total-len(seen)
