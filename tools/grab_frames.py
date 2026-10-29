"""
Grab start and end position photos from each exercise's YouTube demo.

Run from the fmtb-player folder:
    pip install yt-dlp opencv-python
    (ffmpeg must be installed: `brew install ffmpeg` on a Mac)
    python tools/grab_frames.py

What it does, for every exercise video in data/*.json:
  1. Downloads the video (720p max) into tools/cache/.
  2. Finds the first stretch where the body is moving (the first rep).
  3. Saves the frame just before that movement starts as the START photo,
     and the frame that looks most different from it within that rep as the END photo.
  4. Writes images/<video id>-start.webp and -end.webp, and adds
     startPhoto / endPhoto to each exercise in the data files.
  5. Builds tools/review.html so you can check every pair at a glance.

If a pair is wrong (for example it caught you talking to camera), add the exact
seconds to tools/overrides.json and run the script again:
    { "mx-hwFO6Nik": { "start": 12.5, "end": 14.0 } }
"""
import glob, json, os, subprocess, sys

import cv2
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "tools", "cache")
IMAGES = os.path.join(ROOT, "images")
OVERRIDES = os.path.join(ROOT, "tools", "overrides.json")
SAMPLE_FPS = 6          # frames per second to analyse
SKIP_SECONDS = 2.0      # skip the very start of each video
MAX_SECONDS = 60        # only look at the first minute
REP_WINDOW = 5.0        # seconds after motion starts to search for the end position

os.makedirs(CACHE, exist_ok=True)
os.makedirs(IMAGES, exist_ok=True)
overrides = json.load(open(OVERRIDES)) if os.path.exists(OVERRIDES) else {}


def video_ids():
    ids = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "*.json"))):
        data = json.load(open(path))
        for day in data["days"]:
            for sets in day["versions"].values():
                for group in sets:
                    for ex in group["exercises"]:
                        if ex.get("video"):
                            ids.setdefault(ex["video"], ex["name"])
    return ids


def download(vid):
    out = os.path.join(CACHE, vid + ".mp4")
    if not os.path.exists(out):
        subprocess.run(["yt-dlp", "-q", "-f", "bv*[height<=720][ext=mp4]/b[height<=720]",
                        "-o", out, f"https://www.youtube.com/watch?v={vid}"], check=True)
    return out


def read_frames(path):
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    step = max(1, int(round(fps / SAMPLE_FPS)))
    frames, times, i = [], [], 0
    while True:
        ok, frame = cap.read()
        if not ok or i / fps > MAX_SECONDS:
            break
        if i % step == 0 and i / fps >= SKIP_SECONDS:
            frames.append(frame)
            times.append(i / fps)
        i += 1
    cap.release()
    return frames, times


def small_gray(frame):
    g = cv2.cvtColor(cv2.resize(frame, (160, 90)), cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(g, (5, 5), 0).astype(np.float32)


def pick(frames, times):
    g = [small_gray(f) for f in frames]
    motion = np.array([0.0] + [np.abs(g[i] - g[i - 1]).mean() for i in range(1, len(g))])
    smooth = np.convolve(motion, np.ones(3) / 3, mode="same")
    thresh = max(np.percentile(smooth, 60), 1.5)
    moving = np.where(smooth > thresh)[0]
    start = max(0, int(moving[0]) - 1) if len(moving) else 0
    window = [i for i in range(start, len(g)) if times[i] - times[start] <= REP_WINDOW]
    end = max(window, key=lambda i: np.abs(g[i] - g[start]).mean()) if window else start
    return start, end


def frame_at(path, seconds):
    cap = cv2.VideoCapture(path)
    cap.set(cv2.CAP_PROP_POS_MSEC, seconds * 1000)
    ok, frame = cap.read()
    cap.release()
    return frame if ok else None


def save(frame, name):
    h, w = frame.shape[:2]
    scale = 720 / max(h, w)
    if scale < 1:
        frame = cv2.resize(frame, (int(w * scale), int(h * scale)))
    cv2.imwrite(os.path.join(IMAGES, name), frame, [cv2.IMWRITE_WEBP_QUALITY, 82])
    return "images/" + name


def main():
    ids = video_ids()
    results = {}
    for n, (vid, name) in enumerate(ids.items(), 1):
        print(f"[{n}/{len(ids)}] {name} ({vid})")
        try:
            path = download(vid)
            if vid in overrides:
                s, e = overrides[vid]["start"], overrides[vid]["end"]
                fs, fe = frame_at(path, s), frame_at(path, e)
            else:
                frames, times = read_frames(path)
                if not frames:
                    print("   no frames, skipped")
                    continue
                i, j = pick(frames, times)
                fs, fe, s, e = frames[i], frames[j], times[i], times[j]
            results[vid] = {"name": name, "start": save(fs, f"{vid}-start.webp"),
                            "end": save(fe, f"{vid}-end.webp"), "t": [round(s, 1), round(e, 1)]}
        except Exception as err:  # keep going if one video fails
            print("   failed:", err)

    for path in glob.glob(os.path.join(ROOT, "data", "*.json")):
        data = json.load(open(path))
        for day in data["days"]:
            for sets in day["versions"].values():
                for group in sets:
                    for ex in group["exercises"]:
                        r = results.get(ex.get("video"))
                        if r:
                            ex["startPhoto"], ex["endPhoto"] = r["start"], r["end"]
        json.dump(data, open(path, "w"), indent=2)

    rows = "".join(
        f'<div class="r"><h3>{r["name"]} <code>{vid}</code> <small>{r["t"][0]}s → {r["t"][1]}s</small></h3>'
        f'<img src="../{r["start"]}"><img src="../{r["end"]}"></div>' for vid, r in results.items())
    open(os.path.join(ROOT, "tools", "review.html"), "w").write(
        "<meta charset='utf-8'><title>Start and end photos</title><style>body{font:15px system-ui;margin:24px}"
        ".r{margin-bottom:28px}.r img{width:48%;margin-right:2%;border-radius:8px}code{color:#d6307a}</style>"
        "<h1>Check every pair</h1><p>Left is the start position, right is the end. Fix any wrong pair in tools/overrides.json.</p>"
        + rows)
    print(f"\nDone: {len(results)} of {len(ids)} videos. Open tools/review.html to check them.")


if __name__ == "__main__":
    sys.exit(main())
