from time import sleep
import pygame
from tests import SoundManager

pygame.init()

# Create manager
sound_manager = SoundManager()

# Load sounds
sound_manager.load_sound("bell_l", "sound_effects/bell_large.mp3")
sound_manager.load_sound("bell_m", "sound_effects/bell_medium.mp3")
sound_manager.load_sound("sunscreen", "sound_effects/sunscreen_rub.mp3")
sound_manager.load_sound("wooden_clacker", "sound_effects/wooden_clacker.mp3")

# Load music
# sound_manager.load_music("music/background.ogg")
# sound_manager.play_music()
sound_manager.play_sound("bell_l")
sleep(3)
sound_manager.play_sound("bell_m")
sleep(3)
sound_manager.play_sound("sunscreen")
sleep(3)
sound_manager.play_sound("wooden_clacker")
sleep(3)
