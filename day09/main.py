import sys
from collections import deque

path = sys.argv[1] if len(sys.argv) > 1 else "data.txt"
pts = [tuple(map(int, l.split(","))) for l in open(path) if l.strip()]
n = len(pts)


def area(p, q):
    return (abs(p[0] - q[0]) + 1) * (abs(p[1] - q[1]) + 1)


part1 = max(area(pts[i], pts[j]) for i in range(n) for j in range(i + 1, n))

# kompresujemy wspolrzedne
xs = sorted({p[0] for p in pts})
ys = sorted({p[1] for p in pts})
cx = {x: 2 * i + 1 for i, x in enumerate(xs)}
cy = {y: 2 * i + 1 for i, y in enumerate(ys)}
W, H = 2 * len(xs) + 1, 2 * len(ys) + 1

# kody pol
grid = [bytearray(W) for _ in range(H)]
for k in range(n):
    (x1, y1), (x2, y2) = pts[k], pts[(k + 1) % n]
    a1, b1, a2, b2 = cx[x1], cy[y1], cx[x2], cy[y2]
    for yy in range(min(b1, b2), max(b1, b2) + 1):
        for xx in range(min(a1, a2), max(a1, a2) + 1):
            grid[yy][xx] = 1

# zalewamy zewnatrz
grid[0][0] = 2
q = deque([(0, 0)])
while q:
    x, y = q.popleft()
    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == 0:
            grid[ny][nx] = 2
            q.append((nx, ny))

# sumy prefiksowe
pre = [[0] * (W + 1) for _ in range(H + 1)]
for y in range(H):
    row, prow, cur = grid[y], pre[y], pre[y + 1]
    acc = 0
    for x in range(W):
        acc += row[x] == 2
        cur[x + 1] = prow[x + 1] + acc


def outside(x1, y1, x2, y2):
    return pre[y2 + 1][x2 + 1] - pre[y1][x2 + 1] - pre[y2 + 1][x1] + pre[y1][x1]


part2 = 0
for i in range(n):
    for j in range(i + 1, n):
        a = area(pts[i], pts[j])
        if a <= part2:
            continue
        x1, x2 = sorted((cx[pts[i][0]], cx[pts[j][0]]))
        y1, y2 = sorted((cy[pts[i][1]], cy[pts[j][1]]))
        if outside(x1, y1, x2, y2) == 0:
            part2 = a

print("Czesc 1:", part1)
print("Czesc 2:", part2)
