#!/usr/bin/env python3
"""Compare two same-size images. Prints identical pixels, mean absolute difference, bounding box of
differences, and (optionally) saves a diff image.

Usage: python3 pixel_diff.py A.png B.png [--ignore-top 90] [--save diff.png] [--thr 0]
Use it for: before/after pairs (did the screen change?), app page vs Python reference page (is it identical?).
"""
import warnings; warnings.filterwarnings("ignore")
import argparse, sys
from PIL import Image, ImageChops


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a"); ap.add_argument("b")
    ap.add_argument("--ignore-top", type=int, default=0, help="ignore this many pixel rows at the top (status bar clock)")
    ap.add_argument("--thr", type=int, default=0, help="a pixel counts as different if any channel differs by more than this")
    ap.add_argument("--save")
    a = ap.parse_args()
    ia = Image.open(a.a).convert("RGB"); ib = Image.open(a.b).convert("RGB")
    if ia.size != ib.size:
        print("SIZE MISMATCH %s vs %s" % (ia.size, ib.size)); return 2
    if a.ignore_top:
        ia = ia.crop((0, a.ignore_top, ia.width, ia.height)); ib = ib.crop((0, a.ignore_top, ib.width, ib.height))
    d = ImageChops.difference(ia, ib)
    mx = d.point(lambda v: 255 if v > a.thr else 0).convert("L")
    n = sum(1 for v in mx.getdata() if v)
    tot = ia.width * ia.height
    bbox = mx.getbbox()
    mean = sum(sum(px) for px in d.getdata()) / (3.0 * tot)
    print("pixels=%d different=%d (%.3f%%) identical=%.3f%% mean_abs_diff=%.3f bbox=%s" % (tot, n, 100.0 * n / tot, 100.0 * (tot - n) / tot, mean, bbox))
    if a.save:
        d.point(lambda v: min(255, v * 8)).save(a.save)
    return 0 if n == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
