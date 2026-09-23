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
        self.move_delay: float = 0.1
        self.timer: float = 0

        self.death = False
        self.death_timer = 0
        self.death_pause = 1

        self.lives: int = 3
        self.score: int = 0

    def update(self, dt: float) -> bool:
        self.timer += dt
        if self.timer >= self.move_delay:
            self.timer -= self.move_delay
            return True
        else:
            return False

    def queue_direction(self, direction: str) -> None:
        """
        Saves the intended direction for the next game engine tick.
        """
        if direction in ("UP", "DOWN", "LEFT", "RIGHT"):
            self.next_dir = direction

    def enable_cheat_speed(self) -> None:
        """Cheat mode: Pac-Man moves every single engine tick!"""
        self.ticks_per_move = 1

    def next_move(self, direction: str) -> None:
        if direction == "UP":
            self.y -= 1
        elif direction == "DOWN":
            self.y += 1
        elif direction == "LEFT":
            self.x -= 1
        elif direction == "RIGHT":
            self.x += 1

    def add_score(self, score: int) -> None:
        self.score += score

    def respawn(self, dt) -> bool:
        if self.visible is False:
            self.respawn_timer += dt
            if self.death_pause < self.death_timer:
                self.respawn_timer = 0

                return True
            else:
                self.respawn_timer += dt
        return False
