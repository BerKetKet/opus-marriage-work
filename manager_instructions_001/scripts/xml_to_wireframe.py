#!/usr/bin/env python3
"""Turn a uiautomator XML dump into an SVG wireframe plus a table of element sizes (px and dp).

Usage: python3 xml_to_wireframe.py xml/K012.xml wireframes/K012 [--density 2.625] [--min 6]
Writes wireframes/K012.svg and wireframes/K012.md
"""
import argparse, re, sys, xml.etree.ElementTree as ET


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xml")
    ap.add_argument("out")
    ap.add_argument("--density", type=float, default=2.625)
    ap.add_argument("--min", type=int, default=6, help="ignore boxes smaller than this many px")
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=2340)
    a = ap.parse_args()

    root = ET.parse(a.xml).getroot()
    nodes = []
    for n in root.iter("node"):
        m = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", n.get("bounds", ""))
        if not m:
            continue
        x1, y1, x2, y2 = map(int, m.groups())
        if x2 - x1 < a.min or y2 - y1 < a.min:
            continue
        label = n.get("text") or n.get("content-desc") or (n.get("resource-id") or "").split("/")[-1]
        nodes.append(dict(x1=x1, y1=y1, x2=x2, y2=y2, label=label, cls=(n.get("class") or "").split(".")[-1],
                          click=n.get("clickable") == "true", rid=n.get("resource-id") or ""))

    svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" font-family="sans-serif">' % (a.width, a.height, a.width // 2, a.height // 2),
           '<rect width="100%" height="100%" fill="#fff" stroke="#000" stroke-width="2"/>']
    for i, n in enumerate(nodes):
        color = "#1565c0" if n["click"] else "#9e9e9e"
        sw = 3 if n["click"] else 1
        svg.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" stroke-width="%d"/>' % (
            n["x1"], n["y1"], n["x2"] - n["x1"], n["y2"] - n["y1"], color, sw))
        if n["label"] and (n["x2"] - n["x1"]) > 60:
            svg.append('<text x="%d" y="%d" font-size="22" fill="%s">%s</text>' % (n["x1"] + 6, n["y1"] + 26, color, esc(n["label"][:40])))
    svg.append("</svg>")
    open(a.out + ".svg", "w").write("\n".join(svg))

    md = ["# Elements (px and dp at density %.3f)" % a.density, "",
          "| # | label | class | clickable | x1,y1 - x2,y2 (px) | w x h (px) | w x h (dp) |", "|---|---|---|---|---|---|---|"]
    for i, n in enumerate(nodes):
        w, h = n["x2"] - n["x1"], n["y2"] - n["y1"]
        md.append("| %d | %s | %s | %s | %d,%d - %d,%d | %dx%d | %.0fx%.0f |" % (
            i, (n["label"] or "").replace("|", "/")[:40], n["cls"], "yes" if n["click"] else "", n["x1"], n["y1"], n["x2"], n["y2"], w, h, w / a.density, h / a.density))
    open(a.out + ".md", "w").write("\n".join(md) + "\n")
    print("wrote %s.svg and %s.md (%d elements)" % (a.out, a.out, len(nodes)))


if __name__ == "__main__":
    sys.exit(main())
