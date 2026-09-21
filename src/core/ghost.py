class Ghost:
    """
    Represents an AI ghost enemy in the grid.
    Tracks its position, its type (behavior), and its current state.
    """

    def __init__(self, start_x: int, start_y: int, ghost_type: str) -> None:
        # Grid coordinates
        self.x: int = start_x
        self.y: int = start_y

        # Spawn coordinates to return to when eaten
        self.spawn_x: int = start_x
        self.spawn_y: int = start_y

        # "BLINKY", "PINKY", etc. Determines the AI behavior
        self.ghost_type: str = ghost_type

        # Speed expressed in engine ticks required to move
        self.ticks_per_move: int = 2
        self.current_tick_wait: int = 0

        # States could be: "CHASE", "SCATTER", "FRIGHTENED", "DEAD"
        self.state: str = "CHASE"
        self.direction: str = "STOP"

    def update_position(self, new_x: int, new_y: int) -> None:
        """
        Teleports the ghost to the new grid coordinates.
        """
        pass

    def change_state(self, new_state: str) -> None:
        """
        Updates the ghost's behavior state (e.g., becomes edible).
        """
        pass

    def reset_position(self) -> None:
        """
        Teleports the ghost back to its spawn corner.
        """
        pass

    def calculate_next_move(self, target_x: int, target_y: int) -> None:
        """
        AI Logic: Based on its current state and the target coordinates,
        determines which adjacent cell to move to next.
        Returns a tuple (next_x, next_y).
        """
        pass
