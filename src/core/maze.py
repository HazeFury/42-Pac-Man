import random
from dataclasses import dataclass, field

from mazegenerator import MazeGenerator


@dataclass
class Cell:
    """
    Represents a single cell in the maze grid.

    Tracks its coordinates, wall configuration (N, E, S, W),
    and whether it contains entities or items (pacgum, super pacgum).
    """

    x: int
    y: int
    wall: dict[str, bool] = field(
        default_factory=lambda: {"N": True, "E": True, "S": True, "W": True}
    )
    pacgum: bool = False
    super_pacgum: bool = False


class Maze:
    """
    Manages the maze generation, grid representation, and item placement.
    """

    def __init__(
        self, seed: int = 42, w: int = 5, h: int = 5, pacgum: int = 42
    ) -> None:
        """
        Initializes the maze with given dimensions, seed, and pacgum count.
        """
        self.maze = MazeGenerator(size=(w, h), seed=seed)
        self.w = w
        self.h = h
        self.grid: list[list[Cell]] = []

        self.maze_cell_init()
        self.Super_pacgum_placement()
        self.pacgum_placement(pacgum)

    def maze_cell_init(self) -> None:
        """
        Constructs the 2D grid of Cell objects from the generated maze data.
        """
        for pos_y, row_y in enumerate(self.maze.maze):
            row: list[Cell] = []
            for pos_x, col_x in enumerate(row_y):
                row.append((Cell(x=pos_x, y=pos_y, wall=self.wall(col_x))))
            self.grid.append(row)

    def wall(self, bit: int) -> dict[str, bool]:
        """
        Converts bitmask flags into a dictionary of walls (N, E, S, W).
        """
        walls = {
            "N": bool(bit & 1),
            "E": bool(bit & 2),
            "S": bool(bit & 4),
            "W": bool(bit & 8),
        }
        return walls

    def pacgum_placement(self, nb_pacgum: int) -> None:
        """
        Randomly places the requested number of pacgums across available cells.
        """

        if nb_pacgum > self.total_nb_cell():
            print("more pacgum than available Cell filling the whole maze")
            for line in self.grid:
                for cell in line:
                    if cell.super_pacgum is False:
                        if not all(cell.wall.values()):
                            cell.pacgum = True

        else:
            for i in range(nb_pacgum):
                pacgum_assign = False
                while pacgum_assign is False:
                    x, y = (random.randrange(self.w), random.randrange(self.h))
                    self.grid[y][x]
                    if (
                            self.grid[y][x].pacgum is False
                            and self.grid[y][x].super_pacgum is False
                            and not all(self.grid[y][x].wall.values())):
                        self.grid[y][x].pacgum = True
                        pacgum_assign = True

    def total_nb_cell(self) -> int:
        """
        Returns the number of accessible cells available for pacgum placement.
        """
        total_cell = 0
        for line in self.grid:
            for cell in line:
                if not all(cell.wall.values()):
                    total_cell += 1
        return total_cell - 4

    def Super_pacgum_placement(self) -> None:
        """
        Places super pacgums in the four corners of the grid.
        """
        self.grid[0][0].super_pacgum = True
        self.grid[0][self.w - 1].super_pacgum = True
        self.grid[self.h - 1][0].super_pacgum = True
        self.grid[self.h - 1][self.w - 1].super_pacgum = True
