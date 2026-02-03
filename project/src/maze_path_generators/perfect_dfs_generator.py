from src.maze_path_generators.base_generator import MazePathGenerator


class PerfectMazeDFSGenerator(MazePathGenerator):

    def generate(self) -> None:
        stack = []
        visited = set()

        start_cell = self.maze.get_cell_at_position(0, 0)
        stack.append(start_cell)
        visited.add(start_cell)

        while stack:
            current_cell = stack[-1]

            unvisited_neighbors = [
                (neighbor, direction)
                for neighbor, direction
                in self.maze.get_adjacent_cells_with_directions(current_cell)
                if neighbor not in visited and neighbor.is_walkable()
            ]

            if not unvisited_neighbors:
                stack.pop()
                continue

            (neighbor_cell, _) = self.maze.random_number_generator.choice(
                unvisited_neighbors
            )

            self.maze.remove_wall_between_two_adjacent_cells(
                current_cell,
                neighbor_cell
            )

            visited.add(neighbor_cell)
            stack.append(neighbor_cell)
