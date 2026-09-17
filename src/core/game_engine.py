from core.ghost import Ghost
from core.maze import Maze
from core.player import Player


class GameEngine:
    """
    The core logic controller.
    Manages the grid, entities, score, collisions, and the tick-based timeline.
    """

    def __init__(self, level_seed: int = 42) -> None:
        self.running = True
        # Composition: The engine owns the maze and the entities
        self.maze = Maze(seed=level_seed, w=21, h=21, pacgum=150)

        # Hardcoded spawn points for the skeleton (should be dynamic later)
        self.player = Player(
            start_x=self.maze.w // 2, start_y=self.maze.h // 2
        )
        self.ghosts: list[Ghost] = [
            Ghost(start_x=0, start_y=0, ghost_type="BLINKY"),
            Ghost(start_x=19, start_y=0, ghost_type="PINKY"),
        ]

    def update(self, dt: float, key) -> None:
        """
        Updates logic for all entities.
        """
        self.player.update_position(dt, key)

        # Tick timer management
        self.tick_timer: float = 0.0
        # 0.7 seconds between each grid movement
        self.tick_threshold: float = 0.7

        # Game states
        self.is_game_over: bool = False
    #     self.is_victory: bool = False

    # def handle_input(self, direction: str) -> None:
    #     """
    #     Receives input from the View (e.g., "UP", "DOWN")
    #     and queues it in the Player object.
    #     """
    #     pass

    # def update(self, dt: float) -> None:
    #     """
    #     Accumulates delta time. If the threshold is reached, triggers
    #     a game tick.
    #     """
    #     if self.is_game_over or self.is_victory:
    #         return

    #     self.tick_timer += dt
    #     if self.tick_timer >= self.tick_threshold:
    #         self._tick()
    #         self.tick_timer -= self.tick_threshold

    # def _tick(self) -> None:
    #     """
    #     The main logic loop that occurs every X seconds.
    #     Resolves movements, collisions, and consumptions.
    #     """
    #     # 1. Calculate new positions for Player and Ghosts
    #     # 2. Check if moves are valid (no walls) in the Maze
    #     # 3. Apply movements
    #     # 4. Check collisions (Pac-Man vs Ghosts)
    #     # 5. Check item consumption (Pac-Man vs Pacgums)
    #     pass

    # def _handle_collisions(self) -> None:
    #     """
    #     Checks if the Player and any Ghost share the same coordinates.
    #     Applies logic depending on the Ghost's state (lose life or eat ghost).
    #     """
    #     pass

    # def _consume_items(self) -> None:
    #     """
    #     Checks the Maze cell at the Player's coordinates.
    #     If a pacgum is present, increases score and removes it from the Maze.
    #     """
    #     pass
