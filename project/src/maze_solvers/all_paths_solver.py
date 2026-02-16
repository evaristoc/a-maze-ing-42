from src.maze_solvers.base_solver import MazeSolver


class AllPathsSolver(MazeSolver):

    def solve(self) -> list[list]:
        """
        Returns a list of all possible paths from entry to exit.
        Each path is a list of Cells.
        """
        start = self.maze.maze_entry_cell
        goal = self.maze.maze_exit_cell

        all_paths = []

        def dfs(current, path, visited):
            # Goal check (match style of SinglePathSolver)
            if (current.cell_position_x == goal.cell_position_x and
                    current.cell_position_y == goal.cell_position_y):
                all_paths.append(path.copy())
                return

            for neighbor, direction in (
                    self.maze.get_adjacent_cells_with_directions(current)):

                if neighbor is None:
                    continue

                if neighbor in visited:
                    continue

                if not neighbor.is_walkable():
                    continue

                # Match your working solver's wall logic
                opposite_direction = {
                    "north": "south",
                    "east": "west",
                    "south": "north",
                    "west": "east"
                }

                direction = opposite_direction[direction]

                if neighbor.has_wall(direction):
                    continue

                visited.add(neighbor)
                path.append(neighbor)

                dfs(neighbor, path, visited)

                # backtrack
                path.pop()
                visited.remove(neighbor)

        dfs(start, [start], {start})
        return all_paths

    @staticmethod
    def find_shortest_path(paths: list[list]) -> list[list]:
        """
        Takes a list of paths and returns a list containing
        one shortest path (to match SinglePathSolver output type).
        """
        if not paths:
            return []

        shortest = min(paths, key=len)
        return [shortest]

    def solve_shortest(self) -> list[list]:
        """
        Convenience method:
        Finds all paths, then returns only the shortest one.
        """
        all_paths = self.solve()
        return self.find_shortest_path(all_paths)
