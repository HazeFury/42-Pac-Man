from mazegenerator import MazeGenerator
from dataclasses import dataclass, field
import random


@dataclass
class Cell:
    x: int
    y: int
    wall: dict = field(
        default_factory=lambda: {"N": True, "E": True, "S": True, "O": True}
    )
    pacgum: bool = False
    super_pacgum: bool = False
    pacman: bool = False
    ghost: bool = False


class Maze:
    def __init__(self, seed: int = 42, w: int = 5,
                 h: int = 5, pacgum: int = 42) -> None:
        self.maze = MazeGenerator(size=(w, h), seed=seed)
        self.w = w
        self.h = h
        self.grid: list[list[Cell]] = []

        self.maze_cell_init()
        self.Super_pacgum_placement()
        self.pacgum_placement(pacgum)

        for line in self.grid:
            print()
            for cell in line:
                print(f"x:{cell.x} y:{cell.y} pacgum:{cell.pacgum}")

    def maze_cell_init(self):
        for pos_y, row_y in enumerate(self.maze.maze):
            row: list[Cell] = []
            for pos_x, col_x in enumerate(row_y):
                row.append((Cell(x=pos_x, y=pos_y, wall=self.wall(col_x))))
            self.grid.append(row)

    def wall(self, bit: int) -> dict:
        walls = {
            "N": bool(bit & 1),
            "E": bool(bit & 2),
            "S": bool(bit & 4),
            "O": bool(bit & 8)
        }
        return walls

    def pacgum_placement(self, nb_pacgum) -> None:

        if nb_pacgum > self.total_nb_cell():
            print("more pacgum than available Cell filling the whole maze")
            for line in self.grid:
                for cell in line:
                    if cell.super_pacgum is False:
                        cell.pacgum = True

        else:
            for i in range(nb_pacgum):
                pacgum_assign = False
                while pacgum_assign is False:
                    x, y = (random.randrange(self.w), random.randrange(self.h))
                    self.grid[y][x]
                    if (self.grid[y][x].pacgum is False
                            and self.grid[y][x].super_pacgum is False):
                        self.grid[y][x].pacgum = True
                        pacgum_assign = True

    def total_nb_cell(self) -> int:
        total_cell = 0
        for line in self.grid:
            for cell in line:
                if not all(cell.wall.values()):
                    total_cell += 1
        return total_cell - 4

    def Super_pacgum_placement(self):
        self.grid[0][0].super_pacgum = True
        self.grid[0][self.w - 1].super_pacgum = True
        self.grid[self.h - 1][0].super_pacgum = True
        self.grid[self.w - 1][self.h - 1].super_pacgum = True


if __name__ == "__main__":
    Maze()
