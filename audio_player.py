import pygame
from models import Track


class AudioPlayer:
    """Thin wrapper around pygame.mixer.music for MP3 playback."""

    def __init__(self):
        pygame.mixer.init()
        self.current_track: Track | None = None
        self._paused = False

    def play(self, track: Track):
        pygame.mixer.music.load(track.source_path)
        pygame.mixer.music.play()
        self.current_track = track
        self._paused = False

    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self._paused = True

    def resume(self):
        if self._paused:
            pygame.mixer.music.unpause()
            self._paused = False

    def stop(self):
        pygame.mixer.music.stop()
        self.current_track = None
        self._paused = False

    @property
    def is_playing(self) -> bool:
        return pygame.mixer.music.get_busy() and not self._paused

    @property
    def is_paused(self) -> bool:
        return self._paused

    def get_pos(self) -> float:
        """Current playback position in seconds, or -1 if not playing."""
        pos = pygame.mixer.music.get_pos()
        return pos / 1000.0 if pos >= 0 else -1.0

    def cleanup(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()
