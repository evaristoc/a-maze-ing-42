from mazegen.maze_solvers.base_solver import MazeSolver


class SinglePathSolver(MazeSolver):

    def solve(self) -> list[list]:
        start = self.maze.maze_entry_cell
        goal = self.maze.maze_exit_cell

        opposite_direction = {"north": "south",
                              "east": "west",
                              "south": "north",
                              "west": "east"}

        stack = [(start, [start])]
        visited = {start}
        print(stack)
        while stack:
            current, path = stack.pop()

            if (current.cell_position_x == goal.cell_position_x
                ) and (
                    current.cell_position_y == goal.cell_position_y):
                if path is not None:
                    return [path]

            for neighbor, direction in (
                    self.maze.get_adjacent_cells_with_directions(current)):
                # direction = opposite_direction[direction]
                # print(current, neighbor, direction,
                # current.has_wall(direction))
                if neighbor.is_walkable() is not True:
                    continue
                if neighbor in visited:
                    continue
                if neighbor is None:
                    continue
                direction = opposite_direction[direction]
                if neighbor.has_wall(direction):
                    continue

                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))

        return []
