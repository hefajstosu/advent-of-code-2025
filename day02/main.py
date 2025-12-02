import sys

path = sys.argv[1] if len(sys.argv) > 1 else "data.txt"
text = open(path).read().replace("\n", "").strip()
ranges = [tuple(map(int, r.split("-"))) for r in text.split(",") if r]


def invalid_ids(a, b, only_twice):
    # generujemy, nie iterujemy
    found = set()
    for length in range(len(str(a)), len(str(b)) + 1):
        for k in range(2, length + 1):
            if length % k or (only_twice and k != 2):
                continue
            m = length // k
            mult = int(("0" * (m - 1) + "1") * k)  # mnoznik, np. 1001
            lo = max(10 ** (m - 1), -(-a // mult))
            hi = min(10 ** m - 1, b // mult)
            for p in range(lo, hi + 1):
                found.add(p * mult)
    return found


part1 = sum(sum(invalid_ids(a, b, True)) for a, b in ranges)
part2 = sum(sum(invalid_ids(a, b, False)) for a, b in ranges)
print("Czesc 1:", part1)
print("Czesc 2:", part2)
