from dataclasses import dataclass, field
from pathlib import Path

from mutagen.mp3 import MP3
from mutagen.id3 import ID3


@dataclass
class Track:
    source_path: str
    title: str
    duration_secs: float
    original_filename: str

    @classmethod
    def from_file(cls, path: str) -> "Track":
        p = Path(path)
        title = p.stem
        duration = 0.0
        try:
            mp3 = MP3(path)
            duration = mp3.info.length
        except Exception:
            pass
        try:
            tags = ID3(path)
            tit2 = tags.get("TIT2")
            if tit2 and str(tit2):
                title = str(tit2)
        except Exception:
            pass
        return cls(
            source_path=str(p.resolve()),
            title=title,
            duration_secs=duration,
            original_filename=p.name,
        )


@dataclass
class AlbumProject:
    band_name: str = ""
    album_name: str = ""
    tracks: list[Track] = field(default_factory=list)

    @property
    def total_duration(self) -> float:
        return sum(t.duration_secs for t in self.tracks)

    @property
    def remaining(self) -> float:
        return max(0.0, 4800.0 - self.total_duration)

    @property
    def over_limit(self) -> bool:
        return self.total_duration > 4800.0
