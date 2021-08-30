# pycondenser

Tool to make condensed audio for passive immersing. Works with `.ass` and `.srt` subtitles.

Requires `ffmpeg-python`:

```
pip install ffmpeg-python
```

* Does not re-encode audio (ffmpeg -acodec copy)
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
will be created in the same directory.

**Note:** Subtitle and video files should have the
same name. The number of files should be
equal.
