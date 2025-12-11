import sys
from functools import lru_cache

path = sys.argv[1] if len(sys.argv) > 1 else "data.txt"
graph = {}
for line in open(path):
    if ":" in line:
        src, dst = line.split(":")
        graph[src.strip()] = dst.split()


@lru_cache(maxsize=None)
def paths(a, b):
    # liczymy sciezki
    if a == b:
        return 1
    return sum(paths(n, b) for n in graph.get(a, ()))


part1 = paths("you", "out") if "you" in graph else 0
part2 = 0
if "svr" in graph:
    # przez oba wezly
    part2 = (paths("svr", "dac") * paths("dac", "fft") * paths("fft", "out")
             + paths("svr", "fft") * paths("fft", "dac") * paths("dac", "out"))

print("Czesc 1:", part1)
print("Czesc 2:", part2)
