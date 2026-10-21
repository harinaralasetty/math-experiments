"""Part-by-part positive integer DP. No generating functions."""
from collections import defaultdict

def counts(limit, relation):
    states=[defaultdict(int) for _ in range(limit+1)]
    answer=[1]+[0]*limit
    for weight in range(1,limit+1):
        states[weight][weight,weight]=1
    for weight in range(1,limit+1):
        row=states[weight]
        answer[weight]=sum(row.values())
        totals=defaultdict(int)
        for (previous,leader),value in row.items():
            totals[leader]+=value
        for x in range(1,limit-weight+1):
            dest=states[weight+x]
            for leader,total in totals.items():
                equal=row.get((x,leader),0)
                if total!=equal:dest[x,leader]+=total-equal
                allowed={'down': x<leader,'upweak':x>=leader,'downweak':x<=leader}[relation]
                if equal and allowed:dest[x,x]+=equal
        # No future transition reads this row.
        states[weight]=None
    return answer
