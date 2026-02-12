import pygame
from pathlib import Path


class SoundManager:
    def __init__(self, assets_path=None):
        """
        assets_path: path to the assets folder (optional).
        If not provided, it resolves to the sound_assets folder
        next to this file.
        """
        pygame.mixer.init()

        if assets_path is None:
            base_dir = Path(__file__).resolve().parent
            self.assets_path = base_dir / "sound_assets"
        else:
            self.assets_path = Path(assets_path).resolve()

        self.sounds = {}
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        self.music_muted = False
        self.sfx_muted = False

    # -------------------------
    # LOADERS
    # -------------------------

    def load_sound(self, name, relative_path):
        """
        Load a sound effect and store it by name.
        """
        try:
            full_path = self.assets_path / relative_path
            sound = pygame.mixer.Sound(str(full_path))
            sound.set_volume(self.sfx_volume)
            self.sounds[name] = sound
        except Exception as e:
            print(f"[SoundManager] Failed to load sound '{name}': {e}")

    def load_music(self, relative_path):
        """
        Load background music.
        """
        try:
            full_path = self.assets_path / relative_path
            pygame.mixer.music.load(str(full_path))
            pygame.mixer.music.set_volume(self.music_volume)
        except Exception as e:
            print(f"[SoundManager] Failed to load music: {e}")

    # -------------------------
    # PLAYING
    # -------------------------

    def play_sound(self, name):
        if self.sfx_muted:
            return

        sound = self.sounds.get(name)
        if sound:
            sound.play()
        else:
            print(f"[SoundManager] Sound '{name}' not found.")

    def play_music(self, loops=-1):
        if not self.music_muted:
            pygame.mixer.music.play(loops)

    def stop_music(self):
        pygame.mixer.music.stop()

    def pause_music(self):
        pygame.mixer.music.pause()

    def resume_music(self):
        pygame.mixer.music.unpause()

    # -------------------------
    # VOLUME CONTROL
    # -------------------------

    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)

    # -------------------------
    # MUTE TOGGLES
    # -------------------------

    def toggle_music(self):
        self.music_muted = not self.music_muted
        if self.music_muted:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def toggle_sfx(self):
        self.sfx_muted = not self.sfx_muted
