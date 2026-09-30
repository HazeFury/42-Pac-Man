from src.utils.parsing import config


class Player:
    """
    Represents the Pac-Man entity in the grid.
    Only stores coordinates, intended direction, and stats.
    Does NOT handle game logic or maze interaction.
    """

    def __init__(self) -> None:
        """
        Initialize the player position, stats, movement state, and timer.
        """
        self.x: int = 0
        self.y: int = 0
        self.prev_x: float = float(self.x)
        self.prev_y: float = float(self.y)

        self.spawn_x: int = self.x
        self.spawn_y: int = self.y

        # Movement tracking (Buffer logic)
        self.current_dir: str = "NONE"
        self.next_dir: str = "NONE"

        # Speed expressed in engine ticks required to move
        self.move_delay: float = 0.5
        self.timer: float = 0.0

        self.lives: int = config.lives
        self.score: int = 0

    def update(self, dt: float) -> bool:
        """
        Update the movement timer and return True if ready to move.
        """
        self.timer += dt
        if self.timer >= self.move_delay:
            self.timer -= self.move_delay
            return True
        return False

    def get_visual_pos(self) -> tuple[float, float]:
        """
        Returns interpolated (x, y) coordinates between previous and current
        tile positions for 60+ FPS smooth rendering.
        If stopped, returns exact grid coordinates.
        """
        if self.prev_x == self.x and self.prev_y == self.y:
            return (float(self.x), float(self.y))

        duration = 0.5 if self.current_dir == "NONE" else self.move_delay
        if duration > 0:
            progress = min(1.0, max(0.0, self.timer / duration))
        else:
            progress = 1.0

        vis_x = self.prev_x + (self.x - self.prev_x) * progress
        vis_y = self.prev_y + (self.y - self.prev_y) * progress
        return (vis_x, vis_y)

    def queue_direction(self, direction: str) -> None:
        """
        Saves the intended direction for the next game engine tick.
        """
        if direction in ("UP", "DOWN", "LEFT", "RIGHT"):
            self.next_dir = direction

    def next_move(self, direction: str) -> None:
        """
        Save previous position and advance coordinates in given direction.
        """
        self.prev_x = float(self.x)
        self.prev_y = float(self.y)

        if direction == "UP":
            self.y -= 1
        elif direction == "DOWN":
            self.y += 1
        elif direction == "LEFT":
            self.x -= 1
        elif direction == "RIGHT":
            self.x += 1

    def add_score(self, score: int) -> None:
        """
        Add points to the player's total score.
        """
        self.score += score

    def spawn(self, w: int, h: int) -> None:
        """
        Set initial and spawn coordinates at the center of the grid.
        """
        self.spawn_x = ((w // 2) if (w % 2) != 0 else ((w // 2) - 1))
        self.spawn_y = h // 2

        self.x, self.y = self.spawn_x, self.spawn_y
        self.prev_x, self.prev_y = float(self.x), float(self.y)
