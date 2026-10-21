"""Independent anti-run generating functions and pattern checker."""
from functools import lru_cache


def mul(a, b, limit):
    result = [0] * (limit + 1)
    for i, x in enumerate(a):
        if x:
            for j in range(min(len(b) - 1, limit - i) + 1):
                if b[j]:
                    result[i + j] += x * b[j]
    return result


def anti_leaders(limit):
    # q_j = z^j/(1+z^j), D = 1-sum_j q_j.
    # The OGF of a nonempty anti-run starting at L is q_L/D.
    # Its OGF when ending at j != L is q_L*q_j/D.
    # Split at equal neighbors. All next leaders j satisfy j>L, hence
    # F_L = (q_L/D)*(1 + sum_{j>L} q_j*F_j).
    # This counts entire anti-runs, unlike the part-by-part state DP.
    qs = {}
    total = [0] * (limit + 1)
    for j in range(1, limit + 1):
        q = [0] * (limit + 1)
        for k in range(1, limit // j + 1):
            q[j * k] = 1 if k % 2 else -1
            total[j * k] += q[j * k]
        qs[j] = q
    inv = [1] + [0] * limit
    for n in range(1, limit + 1):
        inv[n] = sum(total[k] * inv[n-k] for k in range(1, n+1))
    suffix = [1] + [0] * limit
    answer = [1] + [0] * limit
    for leader in range(limit, 0, -1):
        f = mul(qs[leader], mul(inv, suffix, limit), limit)
        answer = [x + y for x, y in zip(answer, f)]
        extra = mul(qs[leader], f, limit)
        suffix = [x + y for x, y in zip(suffix, extra)]
    return answer


@lru_cache(maxsize=65536)
def normal(word):
    rank = {x: k for k, x in enumerate(sorted(set(word)))}
    return bytes(rank[x] for x in word)


def patterns(n):
    # Independent binary cut-mask generation. Cache only the normalization
    # of individual subwords, never composition counts or expected terms.
    if n == 0:
        return 1
    answer = 0
    for mask in range(1 << (n - 1)):
        parts = []
        start = 0
        while mask:
            bit = mask & -mask
            end = bit.bit_length()
            parts.append(end - start)
            start = end
            mask -= bit
        parts.append(n - start)
        word = tuple(parts)
        found = {b''}
        for i in range(len(word)):
            for j in range(i + 1, len(word) + 1):
                found.add(normal(word[i:j]))
        answer += len(found)
    return answer


def pattern_totals(limit):
    # Each DFS node is one composition. When a part is appended, exactly
    # its suffixes are the new windows. Normalize them by sorting their
    # actual values; no packed-rank arithmetic is used in this checker.
    answer = [0] * (limit + 1)
    word = []
    found = {b''}

    def visit(weight):
        answer[weight] += len(found)
        for x in range(1, limit - weight + 1):
            word.append(x)
            w = tuple(word)
            added = {normal(w[i:]) for i in range(len(w))} - found
            found.update(added)
            visit(weight + x)
            found.difference_update(added)
            word.pop()

    visit(0)
    return answer
