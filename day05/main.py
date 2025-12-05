import sys

path = sys.argv[1] if len(sys.argv) > 1 else "data.txt"
top, bottom = open(path).read().strip().split("\n\n")
ranges = [tuple(map(int, l.split("-"))) for l in top.split()]
ids = [int(x) for x in bottom.split()]

part1 = sum(any(a <= i <= b for a, b in ranges) for i in ids)

# scalamy przedzialy
part2 = 0
cur_a, cur_b = None, None
for a, b in sorted(ranges):
    if cur_b is not None and a <= cur_b + 1:
        cur_b = max(cur_b, b)
    else:
        if cur_b is not None:
            part2 += cur_b - cur_a + 1
        cur_a, cur_b = a, b
if cur_b is not None:
    part2 += cur_b - cur_a + 1

print("Czesc 1:", part1)
print("Czesc 2:", part2)
