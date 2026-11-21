#!/usr/bin/env python3
"""Measure how long a screen transition lasts from a screenrecord video (needs ffmpeg and ffprobe).

Record:  adb shell screenrecord --time-limit 6 /sdcard/m.mp4   (do the gesture ~1.5 s after starting)
Pull:    adb pull /sdcard/m.mp4 motion_x.mp4
Measure: python3 motion_measure.py motion_x.mp4
Prints first-change time, last-change time, duration in ms and the per-frame step (so you can judge the frame rate).
Note: screenrecord only writes frames when the screen changes, so durations are measured between the first and last changed frame.
"""
import subprocess, sys, shutil


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    for t in ("ffmpeg", "ffprobe"):
        if not shutil.which(t):
            print("MISSING TOOL: %s. Install ffmpeg (record it in DECISIONS.md) or label all timings 'est' (estimate)." % t); return 3
    v = sys.argv[1]
    thr = float(sys.argv[2]) if len(sys.argv) > 2 else 1.5
    w, h = 54, 117
    ts = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "frame=pts_time", "-of", "csv=p=0", v], capture_output=True, text=True).stdout.split()
    times = [float(x) for x in ts if x.replace(".", "", 1).isdigit()]
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", v, "-vf", "scale=%d:%d,format=gray" % (w, h), "-f", "rawvideo", "-"], capture_output=True).stdout
    fs = w * h
    n = len(raw) // fs
    if n < 2:
        print("not enough frames"); return 2
    changed = []
    for i in range(1, n):
        a, b = raw[(i - 1) * fs:i * fs], raw[i * fs:(i + 1) * fs]
        m = sum(abs(x - y) for x, y in zip(a, b)) / float(fs)
        if m > thr:
            changed.append(i)
    if not changed:
        print("no change detected between frames"); return 1
    t0 = times[changed[0]] if len(times) == n else changed[0] / 30.0
    t1 = times[changed[-1]] if len(times) == n else changed[-1] / 30.0
    steps = [times[i] - times[i - 1] for i in range(1, len(times))] if len(times) == n else []
    print("frames=%d changed_frames=%d first_change=%.3fs last_change=%.3fs duration_ms=%.0f median_frame_step_ms=%.1f" % (
        n, len(changed), t0, t1, (t1 - t0) * 1000, (sorted(steps)[len(steps) // 2] * 1000 if steps else 0)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
