import sys

path = sys.argv[1] if len(sys.argv) > 1 else "data.txt"
rolls = set()
for r, line in enumerate(open(path)):
    for c, ch in enumerate(line.strip()):
        if ch == "@":
            rolls.add((r, c))

DIRS = [(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if dr or dc]


def neighbours(p):
    return sum((p[0] + dr, p[1] + dc) in rolls for dr, dc in DIRS)


# liczymy samotne rolki
part1 = sum(neighbours(p) < 4 for p in rolls)

# usuwamy do skutku
part2 = 0
queue = list(rolls)
while queue:
    p = queue.pop()
    if p not in rolls or neighbours(p) >= 4:
        continue
    rolls.remove(p)
    part2 += 1
    for dr, dc in DIRS:
        q = (p[0] + dr, p[1] + dc)
        if q in rolls:
            queue.append(q)

print("Czesc 1:", part1)
print("Czesc 2:", part2)
