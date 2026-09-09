# Copyright (C) 2023 github.com/ping
# Chapter-split helper added for odmpy-splitchapters
from __future__ import annotations

import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

import eyed3  # type: ignore[import]
from termcolor import colored

from .shared import sanitize_path, write_tags
from ..errors import OdmpyRuntimeError


def split_into_chapter_mp3s(
    source_filename: Path,
    book_folder: Path,
    chapter_markers: List[Dict],
    title: str,
    sub_title: Optional[str],
    authors: List[str],
    narrators: Optional[List[str]],
    publisher: str,
    description: str,
    cover_bytes: Optional[bytes],
    genres: Optional[List[str]],
    languages: Optional[List[str]],
    published_date: Optional[str],
    series: Optional[str],
    overdrive_id: str,
    isbn: Optional[str],
    audio_bitrate: int,
    ffmpeg_loglevel: str,
    hide_progress: bool,
    id3v2_version: tuple,
    overwrite_tags: bool,
    tag_delimiter: str,
    remove_from_paths: Optional[str],
    logger: logging.Logger,
) -> None:
    """
    Split a merged audiobook into one MP3 per chapter. Leaves the merged file in place.
    """
    if not chapter_markers:
        logger.warning("No chapter markers available; skipped --splitchapters.")
        return
    if not source_filename.exists():
        logger.warning(
            'Merged file "%s" not found; skipped --splitchapters.', source_filename
        )
        return

    chapters_dir = book_folder.joinpath("chapters")
    chapters_dir.mkdir(parents=True, exist_ok=True)
    total = len(chapter_markers)
    logger.info(
        'Splitting "%s" into %s chapter MP3s in "%s"...',
        colored(str(source_filename), "magenta"),
        total,
        colored(str(chapters_dir), "magenta"),
    )

    used_names = set()
    for i, marker in enumerate(chapter_markers, start=1):
        start_second = float(marker.get("start_second") or 0)
        end_second = float(marker.get("end_second") or 0)
        if end_second <= start_second:
            logger.warning(
                "Skipping zero-length chapter %s (%s)",
                i,
                marker.get("title") or "",
            )
            continue

        chapter_title = str(marker.get("title") or f"Chapter {i}").strip()
        safe_title = sanitize_path(
            chapter_title, exclude_chars=remove_from_paths or ""
        ).strip(" .")
        if not safe_title:
            safe_title = f"Chapter {i}"
        base_name = f"{i:03d} - {safe_title}"
        dest_name = f"{base_name}.mp3"
        suffix = 2
        while dest_name.lower() in used_names:
            dest_name = f"{base_name} ({suffix}).mp3"
            suffix += 1
        used_names.add(dest_name.lower())
        dest_filename = chapters_dir.joinpath(dest_name)
        temp_filename = dest_filename.with_suffix(".part.mp3")

        cmd = [
            "ffmpeg",
            "-y",
            "-nostdin",
            "-hide_banner",
            "-loglevel",
            ffmpeg_loglevel,
        ]
        if not hide_progress:
            cmd.append("-stats")
        cmd.extend(
            [
                "-ss",
                f"{start_second:.3f}",
                "-to",
                f"{end_second:.3f}",
                "-i",
                str(source_filename),
                "-vn",
                "-c:a",
                "copy",
                "-map_chapters",
                "-1",
                "-b:a",
                f"{audio_bitrate}k" if audio_bitrate else "64k",
                "-f",
                "mp3",
                str(temp_filename),
            ]
        )
        exit_code = subprocess.call(cmd)
        if exit_code:
            logger.warning(
                "stream copy failed for chapter %s; re-encoding",
                colored(chapter_title, "cyan"),
            )
            cmd_reencode = [
                "ffmpeg",
                "-y",
                "-nostdin",
                "-hide_banner",
                "-loglevel",
                ffmpeg_loglevel,
                "-ss",
                f"{start_second:.3f}",
                "-to",
                f"{end_second:.3f}",
                "-i",
                str(source_filename),
                "-vn",
                "-c:a",
                "libmp3lame",
                "-q:a",
                "2",
                "-map_chapters",
                "-1",
                "-f",
                "mp3",
                str(temp_filename),
            ]
            exit_code = subprocess.call(cmd_reencode)
            if exit_code:
                logger.error(f"ffmpeg exited with the code: {exit_code!s}")
                logger.error(f"Command: {' '.join(cmd_reencode)!s}")
                if temp_filename.exists():
                    temp_filename.unlink()
                raise OdmpyRuntimeError(
                    f"ffmpeg failed while splitting chapter {i}: {chapter_title}"
                )

        temp_filename.replace(dest_filename)

        try:
            audiofile = eyed3.load(dest_filename)
            write_tags(
                audiofile=audiofile,
                title=chapter_title,
                sub_title=sub_title,
                authors=authors,
                narrators=narrators,
                publisher=publisher,
                description=description,
                cover_bytes=cover_bytes,
                genres=genres,
                languages=languages,
                published_date=published_date,
                series=series,
                part_number=i,
                total_parts=total,
                overdrive_id=overdrive_id,
                isbn=isbn,
                overwrite_title=True,
                always_overwrite=True,
                delimiter=tag_delimiter,
            )
            audiofile.tag.save(version=id3v2_version)
        except Exception as e:  # pylint: disable=broad-except
            logger.warning(
                "Error tagging chapter MP3 %s: %s",
                dest_filename.name,
                colored(str(e), "red", attrs=["bold"]),
            )

        logger.info(
            'Saved chapter %s "%s"',
            colored(f"{i:03d}", "cyan"),
            colored(str(dest_filename), "magenta"),
        )
