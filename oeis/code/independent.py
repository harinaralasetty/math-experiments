"""Independent methods for the targets with Python secondary checks."""
from collections import defaultdict
from itertools import groupby

def anti_leader_dp(limit):
    # Build words by weight; retain last part and last anti-run leader.
    states = [defaultdict(int) for _ in range(limit+1)]
    states[0][(0, 0)] = 1
    for weight in range(limit+1):
        for (previous, leader), count in list(states[weight].items()):
            for x in range(1, limit-weight+1):
                if previous == 0:
                    new_leader = x
                elif x == previous:
                    if x <= leader:
                        continue
                    new_leader = x
                else:
                    new_leader = leader
                states[weight+x][x, new_leader] += count
    return [sum(row.values()) for row in states]

def words(n):
    # Cut positions between n units, independent of recursive part enumeration.
    if n == 0:
        yield ()
        return
    for mask in range(1 << (n-1)):
        cut = [0] + [i for i in range(1,n) if mask & (1 << (i-1))] + [n]
        yield tuple(b-a for a,b in zip(cut,cut[1:]))

def run_subsequence_count(n):
    count = 0
    for word in words(n):
        lengths = [sum(1 for _ in g) for _,g in groupby(word)]
        remaining = iter(word)
        count += all(any(x == length for x in remaining) for length in lengths)
    return count

def pattern_count(n):
    count = 0
    for word in words(n):
        matched = {()}
        for i in range(len(word)):
            for j in range(i+1, len(word)+1):
                sub = word[i:j]
                rank = {x: k+1 for k,x in enumerate(sorted(set(sub)))}
                matched.add(tuple(rank[x] for x in sub))
        count += len(matched)
    return count

def strict_parts(total, high=None):
    if not total:
        yield ()
        return
    for x in range(min(total, total if high is None else high), 0, -1):
        for rest in strict_parts(total-x, x-1):
            yield (x,) + rest

def feasible_partition_counts(n):
    # A feasible family uses a globally distinct set of summands. Enumerate
    # that strict partition, then every set partition of its summands and
    # record the block sums. This reverses the reference search direction.
    sums_seen = set()
    for summands in strict_parts(n):
        blocks = []
        def assign(i):
            if i == len(summands):
                sums_seen.add(tuple(sorted(blocks)))
                return
            x = summands[i]
            for j in range(len(blocks)):
                blocks[j] += x
                assign(i+1)
                blocks[j] -= x
            blocks.append(x)
            assign(i+1)
            blocks.pop()
        assign(0)
    return sum(1 not in sums for sums in sums_seen)
