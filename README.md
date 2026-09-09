# odmpy-splitchapters

https://github.com/ndevries84/odmpy-splitchapters

Unofficial fork of [ping/odmpy](https://github.com/ping/odmpy) with `--splitchapters`.
Not affiliated with OverDrive/Libby.

Requires Python >= 3.7 and ffmpeg. License: GPL-3.0-or-later.

## What is on GitHub right now

Smaller package modules are on `main`, including the new chapter splitter:
`odmpy/processing/chapter_split.py`

These large upstream files are not on this repo yet:

- `odmpy/odm.py`
- `odmpy/libby.py`
- `odmpy/processing/shared.py`
- `odmpy/processing/audiobook.py`
- `odmpy/processing/odm.py`
- `odmpy/processing/ebook.py`

Until those land, `pipx install git+https://github.com/ndevries84/odmpy-splitchapters.git` will fail.
You already have a complete unmodified fork at https://github.com/ndevries84/odmpy

## Install the working patched copy on a Mac

```bash
brew install python git ffmpeg pipx
pipx ensurepath

mkdir -p ~/Downloads/odmpy-splitchapters
cd ~/Downloads/odmpy-splitchapters
tar -xzf ~/Downloads/odmpy-splitchapters.tar.gz

pipx uninstall odmpy
pipx install .

odmpy libby --splitchapters -d "/Users/nates-macbook/Downloads/audiobooks"
```

`--splitchapters` keeps one tagged merged `.mp3` and writes per-chapter `.mp3` files in `chapters/`.
