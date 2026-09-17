from core.maze import Maze


class Player:
    """
    Represents the Pac-Man entity in the grid.
    Stores grid coordinates, movement intentions, and player stats.
    """

    def __init__(self, start_x: int, start_y: int) -> None:
        # Grid coordinates
        self.x: int = start_x
        self.y: int = start_y
        self.timer = 0
        self.move_delay = 0.02

        # Spawn coordinates to reset after dying
        self.spawn_x: int = start_x
        self.spawn_y: int = start_y

        # Movement tracking

        self.current_dir: str = "STOP"
        # Stores the player's input until the next engine tick
        self.next_dir: str = "STOP"

        # Game stats
        self.lives: int = 3
        self.score: int = 0

    def queue_direction(self, direction: str) -> None:
        """
        Saves the direction the player wants to take at the next tick.
        """
        pass

    def update_position(self, dt: float, key: str, maze: Maze) -> None:
        """
        Teleports the player to the new grid coordinates.
        """
        movement = {"UP": (0, -1), "RIGHT": (1, 0),
                    "DOWN": (0, 1), "LEFT": (-1, 0), "": (0, 0)}
        self.timer += dt
        if self.timer >= self.move_delay:
            maze_cells = maze.grid
            if key == "UP":
                if maze_cells[self.y][self.x].wall["N"] == True:
                    key = ""
            if key == "DOWN":
                if maze_cells[self.y][self.x].wall["S"] == True:
                    key = ""
            if key == "RIGHT":
                if maze_cells[self.y][self.x].wall["E"] == True:
                    key = ""
            if key == "LEFT":
                if maze_cells[self.y][self.x].wall["W"] == True:
                    key = ""
            self.x += movement[key][0]
            self.y += movement[key][1]
            self.timer -= self.move_delay
            maze_cells[self.y][self.x].pacgum = False

    def lose_life(self) -> None:
        """
        Decrements the life counter.
        """
        pass

    def reset_position(self) -> None:
        """
        Resets the player's coordinates to the initial spawn point.
        """
        pass
