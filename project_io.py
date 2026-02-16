import json
from pathlib import Path
from tkinter import filedialog, messagebox

from models import AlbumProject, Track


def save_project(project: AlbumProject, parent=None) -> str | None:
    path = filedialog.asksaveasfilename(
        parent=parent,
        title="Save Album Project",
        defaultextension=".albumplan",
        filetypes=[("Album Plan", "*.albumplan"), ("All files", "*.*")]
    )
    if not path:
        return None
    data = {
        "band_name": project.band_name,
        "album_name": project.album_name,
        "tracks": [
            {
                "source_path": t.source_path,
                "title": t.title,
                "duration_secs": t.duration_secs,
                "original_filename": t.original_filename,
            }
            for t in project.tracks
        ],
    }
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def load_project(parent=None) -> AlbumProject | None:
    path = filedialog.askopenfilename(
        parent=parent,
        title="Load Album Project",
        filetypes=[("Album Plan", "*.albumplan"), ("All files", "*.*")]
    )
    if not path:
        return None
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    tracks = []
    missing = []
    for td in data.get("tracks", []):
        if not Path(td["source_path"]).exists():
            missing.append(td["original_filename"])
        tracks.append(Track(
            source_path=td["source_path"],
            title=td["title"],
            duration_secs=td["duration_secs"],
            original_filename=td["original_filename"],
        ))
    if missing:
        messagebox.showwarning(
            "Missing files",
            f"These source files were not found:\n" + "\n".join(missing),
            parent=parent,
        )
    return AlbumProject(
        band_name=data.get("band_name", ""),
        album_name=data.get("album_name", ""),
        tracks=tracks,
    )
