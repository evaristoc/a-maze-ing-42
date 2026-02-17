import sys
import os

# Ensure the root directory is in the path so we can find mazegen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# expose mazegen
try:
    from mazegen import (mazegenetor,
                        Cell,
                        FourtyTwoCell,
                        EntryCell,
                        ExitCell,
                        Maze
                        )
except ImportError:
    # This handles cases where mazegen isn't found during build
    pass

from .collect_config_variables import (ConfigParser,
                                       ConfigError)

from .renderer import (MlxContext, Viewport, ImageBuffer, MazeRenderer,
                       loop_handler, exit_loop, key_handler_factory)

from .sound_effects_and_music import SoundManager

__all__ = ["Cell", "FourtyTwoCell", "EntryCell", "ExitCell", "Maze",
        "MlxContext", "Viewport", "ImageBuffer", "MazeRenderer",
        "loop_handler", "exit_loop", "key_handler_factory",
        "SoundManager", "ConfigParser", "ConfigError"]
