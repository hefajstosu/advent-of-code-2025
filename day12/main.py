import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "data.txt"
blocks = open(path).read().strip().split("\n\n")

shapes = []
regions = []
for block in blocks:
    lines = block.strip().split("\n")
    if re.match(r"^\d+:$", lines[0].strip()):
        cells = {(r, c) for r, l in enumerate(lines[1:]) for c, ch in enumerate(l) if ch == "#"}
        shapes.append(cells)
        lines = []
    for l in lines:
        m = re.match(r"^(\d+)x(\d+):(.*)$", l.strip())
        if m:
            regions.append((int(m.group(1)), int(m.group(2)), list(map(int, m.group(3).split()))))


def orientations(cells):
    # obroty i odbicia
    res = set()
    cur = list(cells)
    for _ in range(2):
        for _ in range(4):
            cur = [(c, -r) for r, c in cur]
            mr = min(r for r, _ in cur)
            mc = min(c for _, c in cur)
            res.add(tuple(sorted((r - mr, c - mc) for r, c in cur)))
        cur = [(r, -c) for r, c in cur]
    out = []
    for o in res:
        ar, ac = o[0]
        out.append([(r - ar, c - ac) for r, c in o])
    return out


ORIENTS = [orientations(s) for s in shapes]
SIZES = [len(s) for s in shapes]
NODE_LIMIT = 2_000_000


class TooHard(Exception):
    pass


def fits_exact(w, h, counts):
    # backtracking z dziurami
    holes = w * h - sum(c * s for c, s in zip(counts, SIZES))
    full = (1 << (w * h)) - 1
    counts = list(counts)
    failed = set()
    nodes = [0]

    # maski ulozen
    placements = {}
    for idx in range(w * h):
        r0, c0 = divmod(idx, w)
        for t in range(len(SIZES)):
            masks = []
            for o in ORIENTS[t]:
                cells = [(r0 + dr, c0 + dc) for dr, dc in o]
                if all(0 <= r < h and 0 <= c < w for r, c in cells):
                    masks.append(sum(1 << (r * w + c) for r, c in cells))
            placements[idx, t] = masks

    def go(board, holes):
        if not any(counts):
            return True
        if board == full:
            return False
        key = (board, tuple(counts))
        if key in failed:
            return False
        nodes[0] += 1
        if nodes[0] > NODE_LIMIT:
            raise TooHard
        idx = ((~board) & -(~board)).bit_length() - 1  # pierwsze wolne pole
        for t, cnt in enumerate(counts):
            if not cnt:
                continue
            for mask in placements[idx, t]:
                if not board & mask:
                    counts[t] -= 1
                    res = go(board | mask, holes)
                    counts[t] += 1
                    if res:
                        return True
        if holes > 0 and go(board | (1 << idx), holes - 1):
            return True
        failed.add(key)
        return False

    return go(0, holes)


def fits(w, h, counts):
    total = sum(counts)
    if sum(c * s for c, s in zip(counts, SIZES)) > w * h:
        return False                       # za malo miejsca
    if (w // 3) * (h // 3) >= total:
        return True                        # luzno, zmiesci sie
    try:
        return fits_exact(w, h, counts)
    except TooHard:
        print("Uwaga: region %dx%d nierozstrzygniety, przyjeto test powierzchni" % (w, h),
              file=sys.stderr)
        return True


part1 = sum(fits(w, h, c) for w, h, c in regions)
print("Czesc 1:", part1)
print("Czesc 2: -")
