---
name: video-content-extractor
description: Extract key frames and text content from video files using ffmpeg and Tesseract OCR.
metadata:
  short-description: Extract frames + OCR from videos, output structured MD
---

# Video Content Extractor

Extracts key frames from MP4 videos, runs Tesseract OCR, and generates structured Markdown reports.

## Usage

In Codex CLI, invoke the skill.

## Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| video_path | string | Path to the video file | required |
| output_dir | string | Output directory | same as video |
| interval | integer | Frame interval in seconds | 30 |
| lang | string | OCR language | chi_sim+eng |

## Requirements

- FFmpeg on PATH
- Tesseract OCR with language packs
- Python 3.8+