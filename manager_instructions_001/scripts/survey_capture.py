#!/usr/bin/env python3
"""Capture one state of the reference (Kindle) app: screenshot + uiautomator XML + index row.

Example:
  python3 survey_capture.py K012 "Aa sheet, Theme tab" --path "open book > tap centre > tap Aa" --out specs/kindle_survey
"""
import argparse, datetime, hashlib, pathlib, subprocess, sys


def adb(serial, *args, binary=False, timeout=60):
    cmd = ["adb"] + (["-s", serial] if serial else []) + list(args)
    r = subprocess.run(cmd, capture_output=True, timeout=timeout)
    return r.stdout if binary else r.stdout.decode(errors="ignore")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("title")
    ap.add_argument("--path", default="", help="how this state was reached (taps/gestures)")
    ap.add_argument("--notes", default="")
    ap.add_argument("--out", default="specs/kindle_survey")
    ap.add_argument("--serial", default=None)
    ap.add_argument("--suffix", default="", help="e.g. _bounds when layout bounds are on")
    ap.add_argument("--no-xml", action="store_true")
    a = ap.parse_args()

    out = pathlib.Path(a.out)
    (out / "screens").mkdir(parents=True, exist_ok=True)
    (out / "xml").mkdir(parents=True, exist_ok=True)
    png = adb(a.serial, "exec-out", "screencap", "-p", binary=True)
    if not png.startswith(b"\x89PNG"):
        print("ERROR: screencap did not return a PNG (is the device attached and awake? is the app marked secure?)")
        return 2
    name = a.id + a.suffix
    (out / "screens" / (name + ".png")).write_bytes(png)
    h = hashlib.sha256(png).hexdigest()

    xml_status = "skipped"
    if not a.no_xml:
        xml_status = "FAILED"
        for _ in range(3):
            adb(a.serial, "shell", "uiautomator", "dump", "/sdcard/_survey.xml")
            data = adb(a.serial, "exec-out", "cat", "/sdcard/_survey.xml", binary=True)
            if b"<hierarchy" in data:
                (out / "xml" / (name + ".xml")).write_bytes(data)
                xml_status = "ok"
                break

    idx = out / "INDEX.md"
    if not idx.exists():
        idx.write_text("# Survey index\n\n| id | title | how reached | time | sha256[:12] | xml | notes |\n|---|---|---|---|---|---|---|\n")
    prev = idx.read_text()
    dup = ""
    for line in prev.splitlines():
        cols = [c.strip() for c in line.split("|")]
        if len(cols) > 6 and cols[5] == h[:12]:
            dup = " DUPLICATE-OF-" + cols[1]
    with open(idx, "a") as f:
        f.write("| %s | %s | %s | %s | %s | %s | %s |\n" % (
            name, a.title, a.path, datetime.datetime.now().strftime("%H:%M:%S"), h[:12], xml_status, (a.notes + dup).strip()))
    print("captured %s (%d bytes, xml %s)%s" % (name, len(png), xml_status, dup))
    if dup:
        print("WARNING: identical to an earlier capture. Did the screen actually change?")
    return 0


if __name__ == "__main__":
    sys.exit(main())
