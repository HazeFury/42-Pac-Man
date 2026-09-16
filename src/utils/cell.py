from mazegenerator import MazeGenerator
from dataclasses import dataclass, field


@dataclass
class Cell:
    x: int
    y: int
    wall: dict = field(
        default_factory=lambda: {"N": 1, "E": 1, "S": 1, "O": 1}
    )
    pacgum: bool = False
    super_pacgum: bool = False
    pacman: bool = False
    ghost: bool = False


class Maze:
    def __init__(self, seed: int = 42, w: int = 3, h: int = 3) -> None:
        maze = MazeGenerator(size=(w, h), seed=seed)
        self.grid: list[list[Cell]] = []

        for pos_y, row_y in enumerate(maze.maze):
            row: list[Cell] = []
            for pos_x, col_x in enumerate(row_y):
                row.append((Cell(x=pos_x, y=pos_y, wall=self.wall(col_x))))
            self.grid.append(row)
        print(self.grid)

    def wall(self, bit: int):
        walls = {
            "N": bool(bit & 1),
            "E": bool(bit & 2),
            "S": bool(bit & 4),
            "O": bool(bit & 8)
        }
        return walls


if __name__ == "__main__":
    Maze()
