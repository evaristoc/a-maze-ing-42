from src.maze_solvers.base_solver import MazeSolver


class AllPathsSolver(MazeSolver):

    def solve(self) -> list[list]:
        start = self.maze.maze_entry_cell
        goal = self.maze.maze_exit_cell

        all_paths = []

        def dfs(current, path, visited):
            if current == goal:
                all_paths.append(path.copy())
                return

            for neighbor, direction in (
                    self.maze.get_adjacent_cells_with_directions(current)):

                if neighbor in visited:
                    continue
                if current.has_wall(direction):
                    continue

                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor, path, visited)
                path.pop()
                visited.remove(neighbor)

        dfs(start, [start], {start})
        return all_paths
