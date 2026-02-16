import re
import shutil
from pathlib import Path

from mutagen.id3 import ID3, TIT2, TRCK, TALB, TPE1, ID3NoHeaderError

from models import AlbumProject


def sanitize_filename(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*]', "", name)
    name = name.strip(". ")
    return name or "Untitled"


def export_album(project: AlbumProject, output_dir: Path) -> list[str]:
    """Copy, rename, and tag tracks. Returns list of created paths."""
    if not project.tracks:
        raise ValueError("No tracks to export")
    if not project.album_name.strip():
        raise ValueError("Album name is required")

    # Check duplicate sanitized titles
    titles = [sanitize_filename(t.title) for t in project.tracks]
    seen = {}
    for i, t in enumerate(titles):
        if t in seen:
            raise ValueError(
                f'Duplicate title "{t}" (tracks {seen[t]+1} and {i+1})'
            )
        seen[t] = i

    album_dir = output_dir / sanitize_filename(project.album_name)
    album_dir.mkdir(parents=True, exist_ok=True)

    created = []
    for i, track in enumerate(project.tracks, 1):
        safe_title = sanitize_filename(track.title)
        dest = album_dir / f"{i:02d}. {safe_title}.mp3"
        shutil.copy2(track.source_path, dest)

        # Update ID3 tags
        try:
            tags = ID3(dest)
        except ID3NoHeaderError:
            tags = ID3()
        tags.setall("TRCK", [TRCK(encoding=3, text=str(i))])
        tags.setall("TALB", [TALB(encoding=3, text=project.album_name)])
        if project.band_name.strip():
            tags.setall("TPE1", [TPE1(encoding=3, text=project.band_name)])
        tags.setall("TIT2", [TIT2(encoding=3, text=track.title)])
        tags.save(dest)

        created.append(str(dest))

    return created
