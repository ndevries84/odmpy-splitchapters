# odmpy-splitchapters

Fork of [ping/odmpy](https://github.com/ping/odmpy) with one extra option:

**`--splitchapters`** keeps a tagged merged `.mp3` and also writes one `.mp3` per chapter.

This is an unofficial command-line manager for OverDrive/Libby loans. It is not affiliated with OverDrive. Requires Python >= 3.7. Merging and chapter splitting require [ffmpeg](https://ffmpeg.org/).

## Install

```bash
brew install python git ffmpeg pipx
pipx ensurepath

pipx install git+https://github.com/ndevries84/odmpy-splitchapters.git
```

Or:

```bash
python3 -m pip install git+https://github.com/ndevries84/odmpy-splitchapters.git --upgrade
```

## Download + split on a Mac

```bash
odmpy libby --splitchapters -d "$HOME/Downloads/audiobooks"
```

`--splitchapters` implies `--merge` and `--chapters`, and keeps merge format as `.mp3`.

Result:

```text
~/Downloads/audiobooks/
  Title - Author/
    Title - Author.mp3      # tagged single file (kept)
    chapters/
      001 - Chapter 1.mp3
      002 - Chapter 2.mp3
```

## Other useful commands

```bash
odmpy libby -d "$HOME/Downloads/audiobooks"
odmpy libby --direct --latest 1 --splitchapters -d "$HOME/Downloads/audiobooks"
odmpy libbyreturn
odmpy libbyrenew
odmpy --version
```

First Libby run asks for a setup code from the Libby app:
https://help.libbyapp.com/en-us/6070.htm

## License

GPL-3.0, same as upstream [ping/odmpy](https://github.com/ping/odmpy).
