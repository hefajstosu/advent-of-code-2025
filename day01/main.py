import sys

path = sys.argv[1] if len(sys.argv) > 1 else "data.txt"

pos = 50
part1 = 0
part2 = 0
for line in open(path):
    line = line.strip()
    if not line:
        continue
    d, n = line[0], int(line[1:])
    if d == "R":
        # zliczamy przejscia zera
        part2 += (pos + n) // 100
        pos = (pos + n) % 100
    else:
        # krecimy w lewo
        if pos == 0:
            part2 += n // 100
        elif n >= pos:
            part2 += (n - pos) // 100 + 1
        pos = (pos - n) % 100
    if pos == 0:
        part1 += 1

print("Czesc 1:", part1)
print("Czesc 2:", part2)
