    def get_total_size(self, num_cells_x: int, num_cells_y: int): # utils
        total_w = num_cells_x * self.__total_cell_size - self.__wall_thickness * (num_cells_x - 1)
        total_h = num_cells_y * self.__total_cell_size - self.__wall_thickness * (num_cells_y - 1)
        return total_w, total_h