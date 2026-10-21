"""Independent decomposition into whole maximal anti-runs."""
def multiply(a,b,n):
    out=[0]*(n+1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b[:n-i+1]):
                if y:out[i+j]+=x*y
    return out

def inverse(a,n):
    assert a[0]==1
    b=[1]+[0]*n
    for k in range(1,n+1):
        b[k]=-sum(a[j]*b[k-j] for j in range(1,k+1))
    return b

def counts(n,relation):
    # q_j=z^j/(1+z^j); D=1-sum(q_j).
    # Anti-runs starting at L: q_L/D.
    # Anti-runs starting at L and ending j: delta(L,j)*q_L+q_L*q_j/D.
    # Join whole segments at equal neighbors. Strict descent is triangular.
    # Weak orders also admit j=L: eliminate this self term algebraically.
    qs=[]
    d=[1]+[0]*n
    for j in range(1,n+1):
        q=[0]*(n+1)
        for k in range(1,n//j+1):q[j*k]=(-1)**(k+1)
        qs.append(q)
        d=[x-y for x,y in zip(d,q)]
    accumulated=[1]+[0]*n
    answer=[1]+[0]*n
    order=range(n,0,-1) if relation=='upweak' else range(1,n+1)
    strict_inv=inverse(d,n) if relation=='down' else None
    for j in order:
        q=qs[j-1]
        if relation=='down': inv=strict_inv
        else:
            dq=multiply(d,q,n);qq=multiply(q,q,n)
            inv=inverse([d[k]-dq[k]-qq[k] for k in range(n+1)],n)
        f=multiply(q,multiply(inv,accumulated,n),n)
        answer=[x+y for x,y in zip(answer,f)]
        extra=multiply(q,f,n)
        accumulated=[x+y for x,y in zip(accumulated,extra)]
    return answer
