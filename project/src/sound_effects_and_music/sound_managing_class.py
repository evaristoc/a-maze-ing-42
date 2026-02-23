import os
from pathlib import Path

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame  # noqa: E402


class SoundManager:
    def __init__(self, assets_path: str | None = None) -> None:
        pygame.mixer.init()
        if assets_path is None:
            base_dir = Path(__file__).resolve().parent
            self.assets_path = base_dir / "sound_assets"
        else:
            self.assets_path = Path(assets_path).resolve()
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        self.music_volume: float = 0.5
        self.sfx_volume: float = 0.7
        self.music_muted: bool = False
        self.sfx_muted: bool = False

    # -------------------------
    # LOADERS
    # -------------------------

    def load_sound(self, name: str, relative_path: str) -> None:
        try:
            full_path = self.assets_path / relative_path
            sound = pygame.mixer.Sound(str(full_path))
            sound.set_volume(self.sfx_volume)
            self.sounds[name] = sound
        except Exception as e:
            print(f"[SoundManager] Failed to load sound '{name}': {e}")

    def load_music(self, relative_path: str) -> None:
        try:
            full_path = self.assets_path / relative_path
            pygame.mixer.music.load(str(full_path))
            pygame.mixer.music.set_volume(self.music_volume)
        except Exception as e:
            print(f"[SoundManager] Failed to load music: {e}")

    # -------------------------
    # PLAYING
    # -------------------------

    def play_sound(self, name: str) -> None:
        if self.sfx_muted:
            return
        sound = self.sounds.get(name)
        if sound:
            sound.play()
        else:
            print(f"[SoundManager] Sound '{name}' not found.")

    def play_music(self, loops: int = -1) -> None:
        if not self.music_muted:
            pygame.mixer.music.play(loops)

    def stop_music(self) -> None:
        pygame.mixer.music.stop()

    def pause_music(self) -> None:
        pygame.mixer.music.pause()

    def resume_music(self) -> None:
        pygame.mixer.music.unpause()

    # -------------------------
    # VOLUME CONTROL
    # -------------------------

    def set_music_volume(self, volume: float) -> None:
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume: float) -> None:
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)

    # -------------------------
    # MUTE TOGGLES
    # -------------------------

    def toggle_music(self) -> None:
        self.music_muted = not self.music_muted
        if self.music_muted:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def toggle_sfx(self) -> None:
        self.sfx_muted = not self.sfx_muted
