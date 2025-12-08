import sys

path = sys.argv[1] if len(sys.argv) > 1 else "data.txt"
pts = [tuple(map(int, l.split(","))) for l in open(path) if l.strip()]
n = len(pts)
# przyklad vs prawdziwe
connections = 10 if n <= 20 else 1000

pairs = sorted(
    (sum((a - b) ** 2 for a, b in zip(pts[i], pts[j])), i, j)
    for i in range(n) for j in range(i + 1, n)
)

parent = list(range(n))
size = [1] * n


def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


components = n
part1 = part2 = None
for k, (_, i, j) in enumerate(pairs):
    a, b = find(i), find(j)
    if a != b:
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]
        components -= 1
        if components == 1:
            # wszystko juz polaczone
            part2 = pts[i][0] * pts[j][0]
    if k + 1 == connections:
        sizes = sorted((size[r] for r in range(n) if find(r) == r), reverse=True)
        part1 = sizes[0] * sizes[1] * sizes[2]
    if part1 is not None and part2 is not None:
        break

print("Czesc 1:", part1)
print("Czesc 2:", part2)
