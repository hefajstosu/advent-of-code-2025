import re
import sys
from functools import lru_cache

path = sys.argv[1] if len(sys.argv) > 1 else "data.txt"

# pakujemy w bity
BITS = 16


def solve(lights, buttons, joltage):
    n = len(joltage)
    low = sum(1 << (BITS * i) for i in range(n))         # najmlodsze bity
    guard = sum(1 << (BITS * i + BITS - 1) for i in range(n))
    binc = [sum(1 << (BITS * i) for i in b) for b in buttons]

    # wszystkie podzbiory
    m = len(buttons)
    vec = [0] * (1 << m)
    cost = [0] * (1 << m)
    combos = {}
    for s in range(1 << m):
        if s:
            lb = (s & -s).bit_length() - 1
            vec[s] = vec[s & (s - 1)] + binc[lb]
            cost[s] = cost[s & (s - 1)] + 1
        combos.setdefault(vec[s] & low, []).append((cost[s], vec[s]))

    # swiatla to parzystosc
    target = sum(1 << (BITS * i) for i, ch in enumerate(lights) if ch == "#")
    p1 = min(c for c, _ in combos[target])

    # dzielimy przez dwa
    INF = float("inf")

    @lru_cache(maxsize=None)
    def f(t):
        if t == 0:
            return 0
        best = INF
        for c, v in combos.get(t & low, ()):
            d = (t | guard) - v
            if d & guard == guard:          # bez pozyczki
                r = f((d ^ guard) >> 1)     # przesuwamy bezpiecznie
                if c + 2 * r < best:
                    best = c + 2 * r
        return best

    goal = sum(v << (BITS * i) for i, v in enumerate(joltage))
    return p1, f(goal)


part1 = part2 = 0
for line in open(path):
    line = line.strip()
    if not line:
        continue
    lights = re.search(r"\[([.#]*)\]", line).group(1)
    buttons = [list(map(int, g.split(","))) for g in re.findall(r"\(([\d,]*)\)", line)]
    joltage = list(map(int, re.search(r"\{([\d,]*)\}", line).group(1).split(",")))
    a, b = solve(lights, buttons, joltage)
    part1 += a
    part2 += b

print("Czesc 1:", part1)
print("Czesc 2:", part2)
