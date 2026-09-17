class Player:
    """
    Represents the Pac-Man entity in the grid.
    Only stores coordinates, intended direction, and stats.
    Does NOT handle game logic or maze interaction.
    """

    def __init__(self, start_x: int, start_y: int) -> None:
        self.x: int = start_x
        self.y: int = start_y

        self.spawn_x: int = start_x
        self.spawn_y: int = start_y

        # Movement tracking (Buffer logic)
        self.current_dir: str = "NONE"
        self.next_dir: str = "NONE"

        # Speed expressed in engine ticks required to move
        self.ticks_per_move: int = 1
        self.current_tick_wait: int = 0

        self.lives: int = 3
        self.score: int = 0

    def queue_direction(self, direction: str) -> None:
        """
        Saves the intended direction for the next game engine tick.
        """
        if direction in ("UP", "DOWN", "LEFT", "RIGHT"):
            self.next_dir = direction

    def enable_cheat_speed(self) -> None:
        """Cheat mode: Pac-Man moves every single engine tick!"""
        self.ticks_per_move = 1
