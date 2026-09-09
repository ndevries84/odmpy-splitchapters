# odmpy-splitchapters

Fork of [ping/odmpy](https://github.com/ping/odmpy) with `--splitchapters`:
keep a tagged merged `.mp3` and also write one `.mp3` per chapter.

Repo: https://github.com/ndevries84/odmpy-splitchapters

This is an unofficial OverDrive/Libby tool. Not affiliated with OverDrive.
Requires Python >= 3.7 and [ffmpeg](https://ffmpeg.org/).
License: GPL-3.0 (same as upstream).

## Install on a Mac (complete copy)

GitHub still needs the remaining large source files (`odm.py`, `libby.py`, `processing/*`).
Until those are on `main`, install from the project archive or push that archive into this repo.

```bash
brew install python git ffmpeg pipx
pipx ensurepath

mkdir -p ~/Downloads/odmpy-splitchapters
cd ~/Downloads/odmpy-splitchapters
# extract the archive Grok gave you into this folder, then:

pipx uninstall odmpy   # ignore errors if not installed
pipx install .
```

To make `pipx install git+https://...` work, push the extracted tree:

```bash
cd ~/Downloads/odmpy-splitchapters
git init
git add .
git commit -m "Complete odmpy with --splitchapters"
git branch -M main
git remote add origin https://github.com/ndevries84/odmpy-splitchapters.git
git push -u origin main --force

pipx install git+https://github.com/ndevries84/odmpy-splitchapters.git
```

## Usage

```bash
odmpy libby --splitchapters -d "/Users/nates-macbook/Downloads/audiobooks"
```

`--splitchapters` implies `--merge` and `--chapters` and keeps a single tagged `.mp3`.
Chapter files go in a `chapters/` subfolder next to that merged file.

```bash
odmpy libby --direct --latest 1 --splitchapters -d "/Users/nates-macbook/Downloads/audiobooks"
odmpy libbyreturn
odmpy libbyrenew
```

First Libby run asks for a setup code from the Libby app:
https://help.libbyapp.com/en-us/6070.htm
