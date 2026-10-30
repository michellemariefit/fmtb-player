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

Each phase has its own lesson in the course, and GHL drips the lessons every 30 days. The player is one web page that shows whichever phase the link asks for, so every lesson gets the same code with a different number at the end:

```html
<iframe src="https://michellemariefit.github.io/fmtb-player/#phase-1" style="width:100%;height:1400px;border:0" allow="encrypted-media; picture-in-picture" allowfullscreen></iframe>
```

Change `#phase-1` to `#phase-2` in the Phase 2 lesson, and so on up to `#phase-10`. A link with a phase number shows only that phase and hides the phase picker, so a member in the Phase 3 lesson can't jump ahead. The drip itself is GHL's job: set each module to unlock 30 days after the one before, as the PDFs do today.

For lifetime members, link to the page with no phase number: `https://michellemariefit.github.io/fmtb-player/`. That shows every phase with a picker at the top.

## Build a phase from the Word files

`tools/build_phases.py` reads the gym and home Word files and writes `data/fmtb-phase-N.json`. Put the files in `tools/docx/` (ignored by git) as `gym-03.docx` and `home-03.docx`, then:

```
pip install python-docx pillow
python tools/build_phases.py 3
```

It pulls every exercise, its reps, sets, rest, tempo, YouTube link and thumbnail. Drop sets and 1 1/2 reps get a note. Core finishers without a letter (Plank, CAT) become their own group at the end. Phase names and instruction videos live in the `META` table at the top of the script. Then run `grab_frames.py` for the start and end photos.

## Better start and end photos

The photos from the Word files are small thumbnails. `tools/grab_frames.py` pulls sharp start and end frames from the original exercise recordings.

- `tools/sources.json` maps each exercise's YouTube ID to its original recording in Dropbox, folder `Videos/PREGNANCY/Pregnancy Exercise Library/Fit Mom To Be Workouts`. Two exercises can share one recording (`searchFrom` says where the second one starts).
- Copy those recordings into `tools/cache/` (ignored by git), then run `python tools/grab_frames.py`. Anything not in `sources.json` is downloaded from YouTube with yt-dlp instead.
- It picks the frame just before the first rep starts as the start, and the most different frame within that rep as the end.
- Check every pair in `tools/review.html`. Any it gets wrong (for example, you talking to camera), fix by adding the exact seconds to `tools/overrides.json` and running it again.
- Photos that already exist in `images/` are kept, so a new phase only needs the recordings for exercises that are new. Add those to `sources.json`, put just those files in `tools/cache/`, and run the script. To redo a pair on purpose: `python tools/grab_frames.py --force <video id>`.
- `tools/frames.json` remembers the seconds used for every pair so the review page stays complete.
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

- Barbell Curls (phases 2, 3, 4, 5, 7, 9, 10) and Tubing Flys (phases 3 and 4, home) have no demo video in the Word files, so those cards say "Demo video coming soon" and keep the Word thumbnail.
- Cable Incline Presses on the seated machine (YouTube 03yTjkLx8Bk) has no recording in the Dropbox folder, so it keeps its Word thumbnail.
- Supine Stability Ball Hip Extensions Both Legs Down (Phase 10, Day 2, gym) has no link in the Word file.
