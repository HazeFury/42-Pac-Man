class Player:
    """
    Represents the Pac-Man entity in the grid.
    Stores grid coordinates, movement intentions, and player stats.
    """

    def __init__(self, start_x: int, start_y: int) -> None:
        # Grid coordinates
        self.x: int = start_x
        self.y: int = start_y

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

    def update_position(self, new_x: int, new_y: int) -> None:
        """
        Teleports the player to the new grid coordinates.
        """
        pass

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
