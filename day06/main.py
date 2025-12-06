import sys
from math import prod

path = sys.argv[1] if len(sys.argv) > 1 else "data.txt"
lines = [l.rstrip("\n") for l in open(path)]
while lines and not lines[-1].strip():
    lines.pop()
width = max(len(l) for l in lines)
lines = [l.ljust(width) for l in lines]
rows, ops = lines[:-1], lines[-1]

# dzielimy po spacjach
blocks = []
start = None
for c in range(width + 1):
    empty = c == width or all(l[c] == " " for l in lines)
    if not empty and start is None:
        start = c
    elif empty and start is not None:
        blocks.append((start, c))
        start = None


def apply(op, nums):
    return sum(nums) if op == "+" else prod(nums)


part1 = 0
part2 = 0
for a, b in blocks:
    op = ops[a:b].strip()
    # czytamy wierszami
    part1 += apply(op, [int(r[a:b]) for r in rows])
    # czytamy kolumnami
    nums = []
    for c in range(b - 1, a - 1, -1):
        digits = "".join(r[c] for r in rows).strip()
        if digits:
            nums.append(int(digits))
    part2 += apply(op, nums)

print("Czesc 1:", part1)
print("Czesc 2:", part2)
