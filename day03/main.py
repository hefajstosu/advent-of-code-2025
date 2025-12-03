import sys

path = sys.argv[1] if len(sys.argv) > 1 else "data.txt"
banks = [l.strip() for l in open(path) if l.strip()]


def best(bank, k):
    # zachlannie bierzemy max
    res = []
    start = 0
    for i in range(k):
        end = len(bank) - (k - i) + 1
        window = bank[start:end]
        d = max(window)
        start += window.index(d) + 1
        res.append(d)
    return int("".join(res))


print("Czesc 1:", sum(best(b, 2) for b in banks))
print("Czesc 2:", sum(best(b, 12) for b in banks))
