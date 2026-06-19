# Using web-media-getter with Claude Code & AI agents

This is the agent-facing setup. For the human walkthrough, see the [README](../README.md).

## Install as a Claude Code plugin

From the [ckw-skills](https://github.com/connerkward/ckw-skills) marketplace:

```
/plugin marketplace add connerkward/ckw-skills
/plugin install web-media-getter@connerkward
```

Or add this repo directly as its own marketplace:

```
/plugin marketplace add connerkward/web-media-getter-skill
/plugin install web-media-getter@web-media-getter
```

Once installed, the skill triggers on its own whenever a task needs a real or
archival photo/clip/GIF (a hero image, a texture, reference footage, a reaction
GIF) instead of a generated one. You don't call it by name — describe the asset
you want and the agent runs `webmedia.py` for you.

## The `--json` contract

Agents should always pass `--json`. It emits one normalized record per result on
stdout, so the model can rank, filter, and pick without scraping human-formatted
output.

```bash
python3 webmedia.py "apollo moon landing" --source all --count 8 --json
```

### Record schema

Every result has the same shape regardless of source or media type:

```json
{
  "source": "nasa",
  "title": "…",
  "url": "…",
  "thumb": "…",
  "dl": "…direct media URL, or null when only a page exists…",
  "page_url": "…",
  "author": "…",
  "license": "…",
  "type": "image|video|gif",
  "w": null,
  "h": null
}
```

`dl` is the directly-downloadable media URL. When it is `null`, only a landing
page exists — fall back to `page_url`.

## API keys

The five no-key sources work with zero configuration. Key-gated sources activate
automatically when their env var is present (no config file):

| Env var | Source |
|---|---|
| `PEXELS_API_KEY` | Pexels (images, video) |
| `PIXABAY_API_KEY` | Pixabay (images, video) |
| `KLIPY_API_KEY` | KLIPY (GIFs) |
| `GIPHY_API_KEY` | GIPHY (GIFs) |

In a Claude Code setup these live wherever you keep agent secrets (e.g. a
git-ignored `.env`). Never commit keys.

## Downloads + attribution

`--download` fetches each result's `dl` URL into `--out DIR` and writes an
`attribution.json` sidecar (source, author, license, url, page_url) next to the
files, so provenance travels with the media. The agent should surface that file
to the human rather than discarding it.

## Where this fits in a media pipeline

web-media-getter is the **internet-retrieval** capability — the peer to local
semantic search (e.g. CLIP/SigLIP over your own folders) and to generation
(text-to-image/video). Fan out across all three and rank candidates by relevance
only once a single source demonstrably can't serve the request; don't build that
router prematurely.

### The video caveat

Archival sources (Internet Archive, Library of Congress) host **whole
films/documentaries**, not single shots:

- **Modern single clip** → Pexels / Pixabay (born as short clips, direct MP4).
- **Historical single shot** → retrieve the film here, then extract the shot with
  a scene-detection + semantic-search pass (e.g. PySceneDetect to cut shots, then
  rank keyframes; or a video-understanding API to locate a timestamped moment),
  and cut it with ffmpeg.
