# entry point: instantiates MazeGenerator
# a_maze_ing/__main__.py
from .maze import MazeGenerator
import sys

if __name__ == "__main__":
    size = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    mg = MazeGenerator(size)
    mg.generate()