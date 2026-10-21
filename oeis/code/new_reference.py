"""Stage-2 accelerations of reference methods; no expected terms as answers."""
from collections import defaultdict
from math import gcd
from reference import primes_to


def prime_minima(limit, bound):
    # A minimizer of positive score <= limit has at most limit factors.
    # For any exponent e, a prime outside the first limit primes of its
    # residue class mod e can be replaced by an unused smaller prime in
    # that class. Non-coprime residue classes contain only primes dividing
    # e. This gives a small finite prime set even for very large bounds.
    max_e = bound.bit_length() - 1
    top = max(64, max_e)
    while True:
        primes = primes_to(top)
        complete = True
        for e in range(2, max_e + 1):
            counts = [0] * e
            for p in primes:
                counts[p % e] += 1
            if any(gcd(r, e) == 1 and counts[r] < limit
                   for r in range(1, min(limit, e - 1) + 1)):
                complete = False
                break
        if complete:
            break
        top *= 2
    dp = [1] + [bound + 1] * limit
    residue_counts = [[0] * e for e in range(max_e + 1)]
    for p in primes:
        old = dp[:]
        power, exponent = p * p, 2
        while power <= bound and exponent <= p + 1:
            score = p % exponent
            residue_counts[exponent][score] += 1
            if 0 < score <= limit and residue_counts[exponent][score] <= limit:
                for s in range(limit - score + 1):
                    value = old[s] * power
                    if value < dp[s + score]:
                        dp[s + score] = value
            power *= p
            exponent += 1
    return dp


def anti_leaders(limit):
    # State DP with aggregation over previous part. Equal neighbors start
    # a new anti-run and require a strictly larger leader.
    states = [defaultdict(int) for _ in range(limit + 1)]
    states[0][(0, 0)] = 1
    answer = []
    for weight, row in enumerate(states):
        answer.append(sum(row.values()))
        by_leader = defaultdict(int)
        for (previous, leader), count in row.items():
            by_leader[leader] += count
        for x in range(1, limit - weight + 1):
            dest = states[weight + x]
            for leader, count in by_leader.items():
                same = row.get((x, leader), 0)
                if count != same:
                    dest[x, x if leader == 0 else leader] += count - same
                if same and x > leader:
                    dest[x, x] += same
        # Each weight is consumed once; release large state rows.
        states[weight] = None
    return answer
