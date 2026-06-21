---
name: palmier-pro-shorts
description: >
  Vertical short-form video editing workflow using Palmier Pro (the local
  desktop NLE controlled via MCP) instead of Descript. Produces a 9:16
  vertical clip for YouTube Shorts, Instagram Reels, or TikTok: imports a
  local video file directly (no upload step needed), crops/stacks
  side-by-side dual-monitor recordings (facecam + screen) or crops
  talking-head footage to face, and burns in auto-generated captions.
 
  Trigger this skill whenever the user wants a short, reel, vertical video,
  TikTok clip, or 60-second clip AND mentions Palmier, Palmier Pro, or says
  to use Palmier instead of Descript. Also trigger if Palmier Pro is the
  active/connected video-editing tool and the user asks for a short-form
  edit without naming a tool. For Descript-based shorts editing, use the
  shorts-editor skill instead.
---
 
# Palmier Pro Shorts Editor — 9:16 Vertical
 
Palmier Pro is a **local desktop NLE controlled via MCP** — fundamentally
different from Descript, which is a cloud service. These differences change
the workflow significantly:
 
- **No upload step.** Palmier runs on the user's machine, so local file
  paths (e.g. `/Users/yash/Videos/foo.mp4`) can be passed straight to
  `import_media` via `source.path` — no signed-URL workaround needed. `path`
  and `bytes` imports finalize **synchronously**; only `url` imports are
  async and need `wait_for_job`-style polling (there's no such tool here —
  just re-check `get_media`).
- **No "clean up my footage" AI agent.** Unlike Descript's
  `prompt_project_agent`, Palmier has no built-in filler-word/silence
  removal. Only attempt manual filler-word removal (caption the clip, read
  the transcript, `split_clip` + `remove_clips` around junk) if the user
  explicitly asks — it's labor-intensive. Otherwise just trim obvious dead
  air at the start/end by eye.
- **Canvas size is changeable, but not via MCP.** The project resolution
  (width/height) is a real, user-changeable setting in Palmier Pro — there
  is just no tool exposed to Claude for setting it. **The user has to
  change it themselves inside the app.** Always check `get_timeline` first
  — if `width`/`height` aren't 1080×1920, stop and ask the user to switch
  the project to vertical 1080×1920 (9:16) in-app, then re-check
  `get_timeline` (look for `settingsConfigured: true` and the new
  dimensions) before doing any crop/transform math.
- **No export/render/publish tool.** Nothing equivalent to Descript's
  `publish_project`. Once the timeline edit is done, tell the user to
  export from inside Palmier Pro themselves (File > Export or equivalent).
- **Crop + transform gotcha (confirmed by testing, not guessed):** the
  `transform` box (`centerX/centerY/width/height`) describes where the
  **full, uncropped** source would map onto the canvas. `crop` then reveals
  a window *inside* that box — it does NOT resize or recenter the box to
  fit the cropped content. Naively setting `width:1, height:0.5,
  centerX:0.5` plus a crop produces a pillarboxed result (content stuck to
  one edge, black space on the other), not a full-bleed fill. See Step 5
  for the actual formula to compensate — this is the single easiest thing
  to get wrong in this tool.
---
 
## Step 1 — Always start with get_timeline
 
Call `get_timeline` with no args. It returns the current canvas
`width`/`height`/`fps`, `settingsConfigured`, and any existing tracks/clips.
Use the **returned** resolution for all later math — never assume
1080×1920 until verified.
 
The canvas size is a real, changeable setting — it's just changed in the
Palmier Pro app, not through any tool available here. If it isn't already
1080×1920, tell the user to switch the project/sequence to vertical
(1080×1920, 9:16) inside the app. You can keep importing/inspecting the
source while waiting. Once they confirm, call `get_timeline` again and
check `settingsConfigured: true` with `width: 1080, height: 1920` before
doing any crop/transform math.
 
## Step 2 — Import the source file
 
```
import_media({ source: { path: "<absolute local path>" }, name: "<descriptive name>" })
```
 
Synchronous for local paths. Then call `get_media` to confirm and read
`duration`, `sourceWidth`, `sourceHeight`, `hasAudio`.
 
## Step 3 — Add to timeline & inspect layout
 
Convert source duration to **project** frames (project fps, not source
fps): `durationFrames = round(duration_seconds * project_fps)`.
 
```
add_clips({ entries: [{ mediaRef, startFrame: 0, durationFrames }] })
```
 
This auto-creates a video track + linked audio track.
 
Call `inspect_timeline` with `endFrame` = clip duration and `maxFrames:
8-12` to sample frames across the whole clip. Use this to determine:
 
- **Side-by-side** (source width roughly 2–3.5× the height, e.g.
  3840×1080): dual-monitor recording — identify which half is facecam vs
  screen by eye.
- **Standard talking-head** (source ~16:9, e.g. 1920×1080): single
  speaker, crop to face.
Also use this pass to spot dead air at the very start/end — trim later
with `set_clip_properties` (`trimStartFrame`/`trimEndFrame`).
 
## Step 4 — Pick the segment
 
If the source is already ≤60–75s and stays on-topic throughout (common for
short raw recordings), just use the whole thing. If longer, ask the user
which part is the hook/highlight, or — after running captions (Step 6) —
skim the transcript via `get_timeline`'s `captionGroups` to pick a
self-contained ~60s window, then adjust `durationFrames`/trims.
 
## Step 5 — Crop & position for vertical
 
**Pre-requisite: canvas must already be 1080×1920 (confirmed in Step 1).**
 
### The crop + transform formula (read this before either layout)
 
Because `transform` maps the box for the *full uncropped* source onto the
canvas, and `crop` only reveals a window inside that box, you must inflate
the box and shift its center to compensate, per axis, independently:
 
Given crop insets `[top, right, bottom, left]` (fractions 0–1 of the full
source) and a target rectangle on canvas `[x0,x1] × [y0,y1]` (fractions of
canvas) that you want the cropped content to exactly fill:
 
- Horizontal: `keptW = 1 - left - right`. `width = (x1-x0) / keptW`.
  `boxLeft = x0 - left*width`. `centerX = boxLeft + width/2`.
- Vertical: `keptH = 1 - top - bottom`. `height = (y1-y0) / keptH`.
  `boxTop = y0 - top*height`. `centerY = boxTop + height/2`.
If an axis has no crop on it (`inset0=inset1=0`), the formula collapses to
the obvious `size = target range, center = target center` — i.e. only the
cropped axis needs the inflate/shift treatment.
 
Don't be alarmed if `width` comes out > 1 or `centerX` comes out negative
or > 1 — that's expected; it describes an oversized box that's mostly
off-canvas, with crop revealing just the on-canvas slice.
 
### Layout A — Side-by-side source (facecam + screen)
 
Add a second clip referencing the **same** `mediaRef`, via another
`add_clips` call **omitting `trackIndex`** — that auto-creates a fresh
video track (+ linked audio track) rather than overwriting the first clip.
 
Worked example, confirmed working: 3840×1080 source → 1080×1920 canvas,
each half targeting a 1080×960 box.
 
- Left half (facecam), target `x:[0,1], y:[0.5,1]` (bottom half). Crop
  insets `top0 right0.592 bottom0 left0.092` (centers the middle ≈31.6% of
  the full source width — i.e. the centered portion of just that half).
  Per the formula: `width=1/(1-0.092-0.592)=3.165`, `centerX=-0.092*3.165+3.165/2=1.291`.
  Vertical has no crop so `height=0.5, centerY=0.75` directly.
  Final transform: `{ width: 3.165, height: 0.5, centerX: 1.291, centerY: 0.75 }`.
- Right half (screen), target `x:[0,1], y:[0,0.5]` (top half). Crop insets
  `top0 right0.092 bottom0 left0.592`. Same `width=3.165` (symmetric crop
  amount), `centerX=-0.592*3.165+3.165/2=-0.291`. `height=0.5, centerY=0.25`.
  Final transform: `{ width: 3.165, height: 0.5, centerX: -0.291, centerY: 0.25 }`.
- Apply crop via `set_keyframes({ clipId, property: "crop", keyframes:
  [[0, top, right, bottom, left]] })` — one row at frame 0 = constant value.
- Apply transform via `set_clip_properties({ clipIds: [id], transform: {...} })`.
- Default convention: screen on top, facecam on bottom — flip if the user
  prefers otherwise.
- Mute whichever duplicate clip's linked audio you don't want doubled:
  `set_clip_properties({ clipIds: [linkedAudioId], volume: 0 })`.
**Always recompute from the formula above for the actual source
resolution and crop amounts** — don't reuse the numbers verbatim if the
dimensions or desired crop differ.
 
### Layout B — Standard talking-head (no screen share)
 
To crop the centre ~56% of the width and fill the full 1080×1920 canvas
(target `x:[0,1], y:[0,1]`, no vertical crop):
 
- Crop insets `top0 right0.22 bottom0 left0.22` (tune based on framing).
- Per the formula: `keptW = 1-0.22-0.22 = 0.56`, `width = 1/0.56 = 1.786`,
  `centerX = -0.22*1.786 + 1.786/2 = 0.5` (symmetric crop keeps centerX at
  0.5 — only asymmetric crops shift it). `height=1, centerY=0.5` (no
  vertical crop).
- Final transform: `{ width: 1.786, height: 1, centerX: 0.5, centerY: 0.5 }`.
- This is untested against a live talking-head source so far — verify with
  `inspect_timeline` and nudge insets if the speaker's face isn't framed
  well, recomputing `width`/`centerX` from the formula each time you
  change the insets.
After either layout, `inspect_timeline` again at a few frames to visually
confirm full-bleed framing (no black pillarboxing) before moving on.
 
## Step 6 — Captions
 
```
add_captions({
  centerY: 0.92,          // lower third, close to bottom edge — confirmed readable and clear of the dividing line in a side-by-side layout
  fontSize: 60,            // bigger than the 48 default for vertical mobile viewing
  color: "#FFFFFF",
  fontName: "Helvetica-Bold"
})
```
 
Transcribes on-device and places styled caption clips automatically — no
manual transcript work needed. Omit `clipIds` to auto-detect the primary
spoken track. Set `language` (BCP-47) if the footage isn't English.
 
## Step 7 — Final check
 
`inspect_timeline` across start/middle/end frames to eyeball the finished
composite: layout correct, captions readable, no clipped faces/text, audio
not doubled.
 
## Step 8 — Export (manual)
 
No export/publish tool exists. Tell the user the edit is ready in Palmier
Pro and they need to export/render it themselves from the app — mention
the target resolution (1080×1920) so they pick the right export preset.
 
---
 
## Extracting multiple shorts from one long source
 
Palmier has **no multi-sequence/composition concept** — `get_timeline`
always refers to the single project timeline. If asked for several shorts
from one long recording, you can't make 3 separate "projects"; instead you
lay the 3 edited segments back-to-back on the one timeline and tell the
user the timeline ranges to export separately.
 
1. **Transcribe before picking segments.** Import the long source, add it
   as one full-length scratch clip (`add_clips`, `startFrame: 0,
   durationFrames: full length`), then `add_captions` on it with no
   `clipIds` (auto-detects the one spoken track). This gives you a
   complete transcript via `get_timeline`'s `captionGroups` — page through
   with `startFrame`/`endFrame` windows (~150s of footage per window is a
   safe chunk size to stay under the 200-row-per-group cap). Read the full
   transcript and pick 2-4 self-contained, distinct moments (a clean
   definition, a specific surprising technique, a narrative/news beat —
   look for natural sentence boundaries to cut on, e.g. "So this is what
   X is" or a topic-shift "Now,"/"So,").
2. **Clear the scratch work.** `remove_tracks` for every track index from
   that first `get_timeline` call (caption track + video track + audio
   track) once you've picked your segments and noted their source frame
   ranges. Don't try to reuse the scratch clip's crop/captions — rebuild
   clean per segment.
3. **Lay segments out sequentially.** Pick an output position for each
   segment back-to-back (segment 2 starts where segment 1 ends, etc).
   For each segment: `add_clips` for the facecam/screen pair at the
   **output** `startFrame` with `durationFrames` = segment length (this
   defaults to showing SOURCE frames `[0, length)` — wrong, fix next).
4. **Pull the right source window with `trimStartFrame`.** Call
   `set_clip_properties({ clipIds: [id], trimStartFrame: <sourceSegmentStart> })`
   on each of the pair's clips. This shifts the source in-point so the
   displayed range becomes `[sourceSegmentStart, sourceSegmentStart +
   durationFrames)`, while the clip's timeline position/duration (set in
   step 3) stays put. (No `trimStartFrame` needed if a segment happens to
   start at source frame 0.) Then apply the usual crop + transform formula
   from Step 5, and mute the duplicate audio, same as a single short.
5. **Caption each segment with explicit `clipIds`.** Once there's more
   than one spoken-audio clip on the timeline, `add_captions` auto-detect
   ("omit `clipIds`") is ambiguous — always pass the specific unmuted
   audio clip ID for that segment so it transcribes only that range.
6. **Report exact ranges to the user**, both as output-timeline
   timecodes (so they can scrub/export) and original-source timecodes (so
   they know what was used). There's still no export tool — they export
   each range manually, same limitation as a single short.
---
 
## Tightening duration (and why "remove silences" doesn't mean what it does in Descript)
 
Palmier has no waveform/VAD tool, and in practice the auto-captions from
`add_captions` **tile back-to-back with no exposed gaps** — even across a
9+ minute recording, consecutive caption clips' `startFrame` always equals
the previous one's `startFrame + durationFrames`. So there is no reliable
signal here for literal silence detection; don't promise silence removal
in the Descript sense. Say so directly rather than silently skipping the
request or pretending a cut was silence-based when it wasn't.
 
What IS available and serves the same practical goal (tightening pacing,
hitting a duration target like "under 60s"): cut filler, tangential, or
redundant spoken content using the same multi-piece splicing mechanism as
the multi-short workflow above, but within a single short:
 
1. Read the transcript and identify droppable spans — preamble/throat-
   clearing before the real hook starts, tangential detail not essential
   to *this specific* cut's narrative, redundant restatements, hedging
   asides. Favor cutting whole clauses at clear topic-shift boundaries
   (e.g. "But during all of this," "And essentially what had ended up
   happening is") over mid-clause trims — safer both for not garbling
   meaning and for not relying on fine-grained word-order precision in
   the caption data (caption clips are frame-accurate for audio cuts, but
   their *displayed text order* can be slightly jittery at the
   word-to-word level, so don't trust it for surgical precision below
   the clause level).
2. **Prefer fewer, larger cuts over many tiny ones.** A single well-chosen
   contiguous sub-range (just pick a later start / earlier end) is far
   simpler and more reliable than stitching 4+ fragments. Only resort to
   a multi-piece splice when you genuinely need to preserve a strong
   opening hook AND a satisfying closing line that aren't adjacent in the
   source — and even then, 2-3 pieces (1-2 cuts) is usually enough.
3. Each kept piece becomes its own facecam+screen clip pair with its own
   `trimStartFrame` pointing at that piece's source start, placed
   back-to-back in OUTPUT position (piece 2 starts where piece 1 ends,
   etc) — same mechanics as the multi-short section above, just within
   one short instead of across several.
4. Caption the whole short in **one** `add_captions` call listing every
   piece's unmuted audio clip ID in `clipIds` — no need for one call per
   piece.
5. Compute the final duration (`sum of all piece durationFrames / fps`)
   and sanity-check it against the target before calling it done — don't
   eyeball it.
---
 
## A note on tool reliability
 
A Palmier tool call can occasionally time out with no response (observed:
`get_timeline` and `set_clip_properties` both hung for several minutes
then errored). When that happens, don't assume the call partially applied
— re-check with a fresh `get_timeline` once the connection recovers and
re-apply anything that's missing (e.g. a `trimStartFrame` or `transform`
that didn't show up in the refreshed state) before continuing. Treat the
timeline state as the source of truth over what you think you already
sent.
 
---
 
## Speeding up playback slightly (e.g. "make it a bit faster")
 
`set_clip_properties` has a `speed` field (1.0 = normal, >1.0 = faster).
Two things that aren't obvious from the schema alone, confirmed by testing:
 
- **`speed` and `durationFrames` are independent fields you must reconcile
  yourself.** Setting `speed` alone does not shrink the clip's timeline
  footprint. To actually get a shorter, faster-playing clip that still
  plays the *same* source content, set both in the same call:
  `durationFrames = round(oldDurationFrames / speedMultiplier)`, with
  `trimStartFrame` left untouched. The math works out so the same amount
  of source content is consumed either way — only the timeline footprint
  shrinks.
- **Speed (like other timing fields) propagates to a clip's own linked
  audio automatically**, but a facecam/screen pair in this side-by-side
  layout are in *separate* link groups — apply speed+duration to both the
  facecam clip and the screen clip of a piece, not just one.
- **Downstream pieces need `move_clips` after this.** Shrinking piece 1's
  duration leaves a gap where piece 2 used to start — recompute every
  later piece's new `startFrame` (previous piece's new start + new
  duration) and move both its facecam and screen clips there.
- **Captions must be fully regenerated, not shifted.** The old caption
  clips' timing assumed the original tempo; after a speed change the same
  words land at different frames. `remove_tracks` the caption track(s)
  and rerun `add_captions` with the same `clipIds` — confirmed this
  correctly retranscribes against the new (faster) audio with no manual
  offset math needed.
- A genuinely subtle bump is `speed: 1.05` (5% faster) — noticeable enough
  to tighten pacing, not so much that pitch/voice quality suffers.
---
 
## Real silence removal: use ffmpeg outside Palmier, not a workaround inside it
 
Given the "no VAD tool, captions tile with no gaps" limitation documented
earlier, the actually-correct fix — if the user wants real silence
removal rather than manual filler-cutting — is a **pre-processing pass
with ffmpeg on the raw source file**, before it ever gets imported into
Palmier. This works because ffmpeg runs locally on the user's machine
(same place Palmier reads local paths from) and has a real audio-level
`silencedetect` filter Palmier has no equivalent of.
 
Recipe (verified working, including edge cases, in a sandboxed test
before delivering it to a user):
1. `ffmpeg -i in.mp4 -af silencedetect=noise=-30dB:d=0.6 -f null -` logs
   `silence_start`/`silence_end` pairs to stderr.
2. Parse those into "keep" segments (the complement, with ~0.1-0.15s
   padding left on each side so word onsets/offsets don't get clipped).
3. Build a `trim`/`atrim` + `concat` `filter_complex` from the keep list
   and re-encode once.
4. Handle edge cases explicitly: zero silences found (just copy the file
   through, don't error), and silence that runs to end-of-file (no
   matching `silence_end` gets logged — treat it as ending at the file's
   total duration).
**Critical portability constraint discovered by testing:** the user's
machine is macOS, where the stock `/bin/bash` is 3.2 (no `mapfile`, no
array features newer than that) and the stock `grep` is BSD grep (no
`-P`/PCRE support). A script written with GNU-isms will work when *you*
test it in this Linux sandbox and then silently fail on the user's
machine. Concretely: read line-by-line into arrays with a `while IFS=
read -r` loop instead of `mapfile`; parse the ffmpeg log with `sed -n
's/.../\1/p'` instead of `grep -oP`; do float arithmetic with `awk
'BEGIN{...}'` instead of `bc` (recent macOS has dropped `bc`). Test the
script in this sandbox against a synthetic file built with `ffmpeg -f
lavfi` (tone + `anullsrc` segments concatenated) to validate the actual
cut points and resulting duration before handing it over — don't ship an
untested script just because the syntax looks right.
 
This is a standalone utility, independent of Palmier — hand it to the
user as a script to run once against their raw recording, producing a
cleaned file they then import (Step 2) instead of the original.
 
---
 
## Export only ever renders the whole timeline
 
Confirmed from the actual Export dialog (screenshot, not guessed): Format
/ Codec / Resolution / Frame Rate fields only, no in/out-range field, and
the displayed duration always equals the full timeline length. There is
no way to export just one short from inside Palmier when multiple shorts
live back-to-back on the same timeline (see "Extracting multiple shorts"
above for why they have to).
 
**Workaround: export once, split outside Palmier with ffmpeg.** Same
toolchain as the silence-removal script — the user already has ffmpeg, so
hand them a tiny script that cuts the one combined export into N files at
known timecodes (`seconds = outputStartFrame / fps`), re-encoding (not
`-c copy`) so each cut lands exactly on the boundary rather than the
nearest keyframe. Test it against a synthetic dummy file of the same
total duration before delivering, the same way as the silence script —
confirm each piece's `ffprobe`-reported duration matches the expected
`(endFrame-startFrame)/fps` for that short.
 
---
 
## When add_captions produces text that doesn't match what you expected
 
This bit twice in one session and both times the bug was mine, not
Palmier's — worth checking method, not the tool, first:
 
**Always verify with a disposable scratch clip before assuming a tool
bug.** If transcribed text doesn't match what you expect at a given
`trimStartFrame`, don't conclude `add_captions` is broken and don't just
retry the same call (a literal retry reproduces the identical "wrong"
result if your trim value is actually wrong — that's not evidence of a
flaky tool, it's evidence the input was wrong). Instead: `add_clips` a
small (~300-1800 frame) clip at some far-out, clearly-unused output
position (e.g. `startFrame: 20000+`), set `trimStartFrame` to the value
in question, `add_captions` on just that clip, and read what's actually
there. This is cheap (one small clip, a few seconds of transcription) and
gives ground truth before touching the real timeline.
 
**The actual root cause both times: confusing output-relative frame
numbers with source-relative ones.** `get_timeline`'s caption dump
reports `startFrame` in *output/timeline* coordinates. If a clip has
`trimStartFrame=X` and sits at output `startFrame=Y`, a caption reported
at output frame `F` corresponds to **source** frame `F - Y + X`, not `F`
itself. It's easy to skim a caption dump from a clip that's already
positioned somewhere non-zero on the timeline, spot the line you want,
and copy its `startFrame` directly into a new `trimStartFrame` — that
silently drops the `-Y+X` conversion and points at the wrong few seconds
of source. The failure mode is insidious because the wrong content is
real, coherent transcript text (often from a topic the source covers
elsewhere), so it doesn't look obviously broken on a quick visual check —
it takes noticing the actual *words* don't match the intended narrative.
Safest practice: only ever read frame numbers for new `trimStartFrame`
values from a dump where the clip sits at output `startFrame: 0` with no
trim of its own (so output coordinates equal source coordinates 1:1) —
i.e. the disposable-scratch-clip method above, not a repositioned clip
already on the real timeline.
 
---
 
## Common issues
 
- **Any tool returns "Editor not available"** — Palmier Pro app isn't open
  or connected. Ask the user to open it and retry.
- **`canGenerate: false`** — only matters for `generate_video` /
  `generate_image` / `upscale_media`; not needed for a plain
  import+crop+caption short. If the user wants AI b-roll/upscaling, they
  need to sign into Palmier and subscribe first.
- **Picture is pillarboxed/misaligned after cropping (content stuck to
  one edge, black space on the other)** — this is the crop+transform
  gotcha from the overview: you set `width`/`height` as if the box should
  match the cropped content's box size, but the box actually represents
  the *full uncropped* source. Recompute `width`/`height`/`centerX`/`centerY`
  with the formula in Step 5 instead of guessing — this is not a stretch
  problem, no aspect-ratio tweaking will fix it.
- **Captions overlapping the dividing line in side-by-side layout** —
  lower `centerY` a bit (e.g. 0.84), or rerun `add_captions` (it replaces
  caption clips on a fresh track each time).
- **Long source, want a highlight only** — Palmier has no semantic
  "find the best segment" tool. Ask the user where the hook is, or caption
  the full clip first and skim the transcript, then trim and remove
  out-of-range caption clips before repositioning.
- **Canvas isn't 1080×1920 and you proceeded anyway** — stop; don't guess.
  Ask the user to set it in-app. Crop/transform math computed against the
  wrong canvas size produces a broken composite.
 