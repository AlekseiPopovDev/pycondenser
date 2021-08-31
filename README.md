# pycondenser

Tool to make condensed audio for passive immersion.
Works with `.ass` and `.srt` subtitles.

Requires `ffmpeg` and `ffmpeg-python`

Get `ffmpeg` with your package manager. Get `ffmpeg-python` with pip:

```
pip install ffmpeg-python
```

## Features

* Does not re-encode audio (-acodec copy)
* Detects multiple audio streams, prompts user
to select desired one
* Ignores repeated voice lines and voice lines
shorter than one second

## Usage

```
chmod +x pycondenser.py
mv pycondenser.py ~/.local/bin/pycondenser
```

Add `~/.local/bin` directory to PATH if it is not on PATH.

Start `pycondenser` in directory containing
subtitle and video files. Condensed files
by default will be created in the `condensed`
directory.

**Note:** Subtitle and video files should have the
same name. The number of files should be
equal.
