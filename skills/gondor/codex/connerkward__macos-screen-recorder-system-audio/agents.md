# Using sck-record with Claude Code & AI agents

This tool also ships as a Claude Code skill, so an agent can record the screen
(with system audio) on its own. For the human walkthrough, see the
[README](../README.md).

## Install as a Claude Code plugin

Add this repo as its own marketplace:

```
/plugin marketplace add connerkward/macos-screen-recorder-system-audio
/plugin install macos-screen-recorder@macos-screen-recorder
```

Or pull it in as part of the full set:

```
/plugin marketplace add connerkward/connerkward-skills
```

Or just drop this repo's `SKILL.md` into your agent's skills directory.

## What the agent gets

Once installed, the skill triggers when a task needs a scripted screen recording
**with system sound** on macOS — demos, captures, recording a `say`/TTS voice
playing through the speakers — the case `screencapture -v` and QuickTime can't
cover without a virtual audio device.

The skill drives the same single command a human runs:

```
./sck-record <out.mp4> <seconds>
```

## Build note for automated setups

The compiled `sck-record` binary is gitignored. An agent (or a machine-setup
script) builds it once from source:

```sh
swiftc -O sck-record.swift -o sck-record
```

After that, the binary is reused. The first recording still needs the one-time
**Screen Recording** permission granted to whatever app shells out the command —
see [Permissions in the README](../README.md#permissions).

## Where it fits

`sck-record` is the raw capture primitive — it captures, nothing more. The
record-then-polish workflow is a separate layer that *consumes* its output:

- **Polish companion** → [screenstudio-alternative-skill](https://github.com/connerkward/screenstudio-alternative-skill).
  Record with `sck-record --no-cursor out.mp4 N` (so the polish pass can draw its own
  smoothed synthetic cursor), then run its `polish.py` / `render.py` for idle
  speed-up, auto-zoom, keystroke chips, and 9:16 vertical export.
- **The boundary:** auto-zoom and keystroke chips need an input-event log captured
  *at record time* — `sck-record` does not produce one (it records pixels + audio).
  Pixel-only features (idle speed-up via freeze detection, cursor smoothing, vertical
  reframe) work on any `sck-record` mp4; the event-driven features need the companion
  skill's capture-time logger running alongside.

Keep this tool narrow on purpose: one binary, one job — screen + system audio to mp4.
