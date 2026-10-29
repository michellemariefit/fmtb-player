# Fit Mom To Be workout player

One mobile web page that replaces the monthly gym and home PDFs.

## What's here

- `index.html` is the player. It reads one data file per phase.
- `data/fmtb-phase-1.json` and `data/fmtb-phase-2.json` hold every exercise: name, reps, sets, rest, tempo, YouTube demo ID and photo.
- `images/` holds the start and end photos pulled from the Word files.

## Put it online (GitHub Pages)

1. Create a new GitHub repo, for example `fmtb-player`, and upload this whole folder.
2. In the repo, go to Settings, then Pages. Set the source to the `main` branch, root folder.
3. The player goes live at `https://<your-username>.github.io/fmtb-player/`.
4. Open a phase with `#phase-1` or `#phase-2` at the end of the link.

## Put it in GHL

In each phase lesson, add a custom code block with:

```html
<iframe src="https://<your-username>.github.io/fmtb-player/#phase-1" style="width:100%;height:1400px;border:0" allow="encrypted-media; picture-in-picture" allowfullscreen></iframe>
```

Change `#phase-1` to match the lesson.

## Add the next phases (in Claude Code)

Give Claude Code this folder plus the Dropbox Word files for the next phase and ask:

> Read the gym and home Word files for Phase 3. Pull every exercise, its YouTube link and its photo, and write `data/fmtb-phase-3.json` in the same shape as `fmtb-phase-2.json`. Save the photos to `images/` as WebP. Add 3 to the `PHASES` list in `index.html`.

## Better start and end photos

The photos from the Word files are small thumbnails. `tools/grab_frames.py` pulls sharp start and end frames straight from each YouTube demo.

In Claude Code, from this folder:

> Install yt-dlp, opencv-python and ffmpeg, then run `python tools/grab_frames.py`. When it finishes, open `tools/review.html` and show me any pairs that look wrong.

- It picks the frame just before the first rep starts as the start, and the most different frame within that rep as the end.
- Check every pair in `tools/review.html`. Any it gets wrong (for example, you talking to camera), fix by adding the exact seconds to `tools/overrides.json` and running it again.
- The player shows the two photos side by side with Start and End labels as soon as they exist.

## Phase instruction videos

Pulled from the GHL lessons. Put each one in `instructionVideo` when you add that phase.

| Phase | Name | YouTube ID |
| --- | --- | --- |
| 1 | The Full Body Toner | WJV-1d8yLRo (FAQ: BISvZCLwFns) |
| 2 | The Lean Mama | A_ZgsAq8Ckw |
| 3 | Toned Up Prego | ehr6YV-cIrA |
| 4 | The Lean Mean Baby Making Machine | UDQ7Rc7ps-E |
| 5 | Strong Bod Champ | jO-BLhLEL9A |
| 6 | Leveled Up Prego | kO5UMYU2OW0 |
| 7 | Fit Mama Blast | 9pFmm1rq45g |
| 8 | The Lean Mama Slay | -lFGJfiaMXs |
| 9 | The Strong Mama Blast | ipKjuf0IvXs |
| 10 | The Chiseled Mom Workout | 4DPwbPldYew |

## Still to fill in

- Barbell Curl Close Grip (Phase 2, Day 3, gym and home) has no demo video in the Word files.
- The photos are small thumbnails from the Word files. Higher-resolution versions would look sharper on newer phones.
