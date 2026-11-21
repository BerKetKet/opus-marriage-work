#!/usr/bin/env python3
"""Build opus_marriage_work_worker_report_NNN.zip from a staging folder.

The staging folder must contain REPORT.md. Screenshots live in <staging>/screenshots/ and every
image needs one line in <staging>/screenshots/DESCRIPTIONS.tsv (file<TAB>what it shows).
The script refuses duplicates, forbidden file types, forbidden strings, missing descriptions,
near-blank/black images (unless the description starts with EXPECTED-BLANK:), and before/after pairs
that did not really change (screenshots/PAIRS.tsv: before<TAB>after<TAB>min_changed_pixels). It also records the git state of both subfolders.
"""
import warnings; warnings.filterwarnings("ignore")
import argparse, hashlib, os, re, struct, subprocess, sys, zipfile, pathlib

FORBIDDEN_EXT = {".ttf", ".otf", ".bin", ".dic", ".so", ".a", ".apk", ".aar", ".xz", ".zip", ".jar"}
IMG_EXT = {".png", ".jpg", ".jpeg"}
TEXT_EXT = {".md", ".txt", ".json", ".tsv", ".xml", ".log", ".diff", ".patch", ".kt", ".rs", ".py", ".sh", ".svg", ".html", ".toml", ".kts", ".csv"}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def png_dims(p):
    with open(p, "rb") as f:
        d = f.read(24)
    if d[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", d[16:24])
    return None


def blank_stats(p):
    try:
        from PIL import Image, ImageStat
    except Exception:
        return None
    try:
        im = Image.open(p).convert("L")
        im.thumbnail((200, 400))
        s = ImageStat.Stat(im)
        return s.mean[0], s.stddev[0]
    except Exception:
        return None


def git(root, sub, *args):
    try:
        r = subprocess.run(["git", "-C", str(root / sub), *args], capture_output=True, text=True, timeout=60)
        return r.stdout.strip() or r.stderr.strip()
    except Exception as e:
        return "git failed: %s" % e


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", required=True, help="report number, e.g. 002")
    ap.add_argument("--root", default="/home/bgg/projects/opus_marriage_work")
    ap.add_argument("--staging", required=True, help="staging folder (relative to root or absolute)")
    ap.add_argument("--forbid", action="append", default=[], help="string that must not appear in any text file (e.g. device serial)")
    ap.add_argument("--max-mb", type=float, default=25.0)
    a = ap.parse_args()

    root = pathlib.Path(a.root)
    st = pathlib.Path(a.staging)
    if not st.is_absolute():
        st = root / st
    errors, warns = [], []
    if not (st / "REPORT.md").exists():
        errors.append("REPORT.md missing in staging folder")

    patches = st / "patches"
    patches.mkdir(exist_ok=True)
    lines = []
    for sub in ("opus-reader", "render.engine"):
        lines.append("== %s ==" % sub)
        lines.append("branch/status:\n" + git(root, sub, "status", "-sb"))
        lines.append("remotes:\n" + git(root, sub, "remote", "-v"))
        lines.append("log (last 40):\n" + git(root, sub, "log", "--oneline", "-n", "40"))
        lines.append("")
    (patches / "git_state.txt").write_text("\n".join(lines))

    desc = {}
    dpath = st / "screenshots" / "DESCRIPTIONS.tsv"
    if dpath.exists():
        for ln in dpath.read_text().splitlines():
            if "\t" in ln:
                k, v = ln.split("\t", 1)
                desc[k.strip()] = v.strip()

    rows, seen = [], {}
    for p in sorted(st.rglob("*")):
        if not p.is_file() or p.name == "MANIFEST.md":
            continue
        rel = p.relative_to(st).as_posix()
        ext = p.suffix.lower()
        if ext in FORBIDDEN_EXT:
            errors.append("forbidden file type: " + rel)
            continue
        h = sha(p)
        flags = []
        dims = ""
        if ext in IMG_EXT:
            d = png_dims(p) if ext == ".png" else None
            dims = "%dx%d" % d if d else ""
            if h in seen:
                errors.append("DUPLICATE image content: %s == %s" % (rel, seen[h]))
            seen.setdefault(h, rel)
            if p.name not in desc and rel not in desc and p.name != "DESCRIPTIONS.tsv":
                errors.append("image has no description in screenshots/DESCRIPTIONS.tsv: " + rel)
            bs = blank_stats(p)
            dtext = desc.get(p.name, desc.get(rel, ""))
            if bs and (bs[1] < 6.0 or (bs[0] < 10.0 and bs[1] < 20.0)):
                if dtext.startswith("EXPECTED-BLANK:"):
                    flags.append("EXPECTED-BLANK")
                else:
                    errors.append("near-blank or black image (mean %.1f, stddev %.1f): %s. Retake it, or start its description with EXPECTED-BLANK: if blank is the subject" % (bs[0], bs[1], rel))
                    flags.append("BLANK")
        if ext in TEXT_EXT:
            try:
                t = p.read_text(errors="ignore")
            except Exception:
                t = ""
            for fb in a.forbid:
                if fb and fb in t:
                    errors.append("forbidden string %r found in %s" % (fb, rel))
        rows.append((rel, p.stat().st_size, h[:12], dims, ",".join(flags)))

    pairs = st / "screenshots" / "PAIRS.tsv"
    if pairs.exists():
        try:
            from PIL import Image, ImageChops
        except Exception:
            Image = None
            warns.append("PIL missing: PAIRS.tsv not checked")
        if Image:
            for ln in pairs.read_text().splitlines():
                parts = ln.split("\t")
                if len(parts) < 3 or ln.startswith("#"):
                    continue
                b, c, mn = parts[0].strip(), parts[1].strip(), int(parts[2])
                try:
                    ia = Image.open(st / "screenshots" / b).convert("RGB")
                    ib = Image.open(st / "screenshots" / c).convert("RGB")
                    if ia.size != ib.size:
                        errors.append("pair %s/%s: different sizes" % (b, c))
                        continue
                    d = ImageChops.difference(ia, ib).convert("L")
                    d = d.crop((0, 90, d.width, d.height))
                    n = sum(1 for v in d.getdata() if v > 16)
                    if n < mn:
                        errors.append("pair %s -> %s changed only %d pixels below the status bar (needs >= %d): the screen did not really change" % (b, c, n, mn))
                    else:
                        print("pair ok: %s -> %s changed %d pixels" % (b, c, n))
                except Exception as e:
                    errors.append("pair %s/%s unreadable: %s" % (b, c, e))
    if errors:
        print("ERRORS (%d):" % len(errors))
        for e in errors:
            print("  -", e)
    if warns:
        print("WARNINGS (%d):" % len(warns))
        for w in warns:
            print("  -", w)
    if errors:
        print("Report NOT built. Fix the errors above and run again.")
        return 2

    man = ["# MANIFEST (generated by make_report.py)", "", "| file | bytes | sha256[:12] | dims | flags |", "|---|---|---|---|---|"]
    for r in rows:
        man.append("| %s | %d | %s | %s | %s |" % r)
    if warns:
        man += ["", "## Warnings", ""] + ["- " + w for w in warns]
    (st / "MANIFEST.md").write_text("\n".join(man) + "\n")

    out = root / "deliverables" / ("opus_marriage_work_worker_report_%s.zip" % a.n)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(st.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(st).as_posix())
    mb = out.stat().st_size / 1e6
    print("built %s (%.1f MB, %d files)" % (out, mb, len(rows) + 1))
    if mb > a.max_mb:
        print("WARNING: larger than %.0f MB; split the report or remove large files." % a.max_mb)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
