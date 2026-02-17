from collections import deque
from mazegen.maze_solvers.base_solver import MazeSolver


class ShortestPathSolver(MazeSolver):

    def solve(self) -> list[list]:
        start = self.maze.maze_entry_cell
        goal = self.maze.maze_exit_cell

        opposite_direction = {
            "north": "south",
            "east": "west",
            "south": "north",
            "west": "east"
        }

        queue = deque([(start, [start])])
        visited = {start}

        while queue:
            current, path = queue.popleft()

            if (current.cell_position_x == goal.cell_position_x and
                    current.cell_position_y == goal.cell_position_y):
                return [path]

            for neighbor, direction in (
                    self.maze.get_adjacent_cells_with_directions(current)):

                if neighbor is None:
                    continue

                if neighbor in visited:
                    continue

                if not neighbor.is_walkable():
                    continue

                direction = opposite_direction[direction]

                if neighbor.has_wall(direction):
                    continue

                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

        return []
