import sys
from collections import defaultdict

path = sys.argv[1] if len(sys.argv) > 1 else "data.txt"
grid = [l.rstrip("\n") for l in open(path) if l.strip()]

# liczymy linie czasu
beams = {grid[0].index("S"): 1}
splits = 0
for row in grid[1:]:
    nxt = defaultdict(int)
    for c, cnt in beams.items():
        if 0 <= c < len(row) and row[c] == "^":
            splits += 1
            nxt[c - 1] += cnt
            nxt[c + 1] += cnt
        else:
            nxt[c] += cnt
    beams = nxt

print("Czesc 1:", splits)
print("Czesc 2:", sum(beams.values()))
