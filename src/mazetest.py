from mazegenerator import MazeGenerator

TILES = {
    0: ["+   ", "    "],
    1: ["+---", "    "],
    2: ["+   ", "    "],
    3: ["+---", "    "],
    4: ["+   ", "    "],
    5: ["+---", "    "],
    6: ["+   ", "    "],
    7: ["+---", "    "],
    8: ["+   ", "|   "],
    9: ["+---", "|   "],
    10: ["+   ", "|   "],
    11: ["+---", "|   "],
    12: ["+   ", "|   "],
    13: ["+---", "|   "],
    14: ["+   ", "|   "],
    15: ["+---", "|   "],
}


class maze(MazeGenerator):
    def __init__(self, size: tuple[int, int] = (15, 15), perfect: bool = False, entry_cell: tuple[int, int] = (
            0, 0), exit_cell: tuple[int, int] = (-1, -1), seed: int = 0) -> None:
        super().__init__(size, perfect, entry_cell, exit_cell, seed)

        test = MazeGenerator(size=(15, 15))
        print(test.maze)

        for f in test.maze:
            for i in range(2):
                lime = [TILES[n][i] for n in f]
                line = "".join(lime)
                if i == 0:
                    line += "+"
                else:
                    line += "|" if (f[-1] & 2) else " "

                print(line)
        bottom = "".join(
            ["+---" if (n & 4) else "+   " for n in test.maze[-1]]) + "+"

        print(bottom)


if __name__ == "__main__":
    maze()
