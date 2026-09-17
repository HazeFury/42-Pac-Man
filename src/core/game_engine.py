from core.ghost import Ghost
from utils.input_manager import InputManager
from core.maze import Maze
from core.player import Player


class GameEngine:
    """
    The core logic controller (Model).
    Manages the grid, entities, score, collisions, and the tick-based timeline.
    """

    def __init__(self, level_seed: int = 42) -> None:
        self.running = True
        self.maze = Maze(seed=level_seed, w=21, h=21, pacgum=1000)

        self.player = Player(
            start_x=self.maze.w // 2, start_y=self.maze.h // 2
        )
        self.ghosts: list[Ghost] = []
        self.input_manager = InputManager()

        # Tick timer management
        self.tick_timer: float = 0.0
        # Reduced to 0.25s for a more playable Pac-Man speed
        self.tick_threshold: float = 0.25

        self.is_game_over: bool = False

    def handle_input(self) -> None:
        """
        Receives input from the Controller/View and queues it.
        """
        direction: str = self.input_manager.get_movement_intention()
        self.player.queue_direction(direction)

    def update(self, dt: float) -> None:
        """
        Accumulates delta time and triggers a game tick when the
        threshold is met.
        """
        if self.is_game_over:
            return

        self.tick_timer += dt
        if self.tick_timer >= self.tick_threshold:
            self._tick()
            self.tick_timer -= self.tick_threshold

    def _tick(self) -> None:
        """
        Main logic loop executed rapidly (e.g., every 0.1 seconds).
        Only entities whose wait timer has reached 0 are allowed to move.
        """
        # --- Handle Player ---
        if self.player.current_tick_wait <= 0:
            self._resolve_player_movement()
            # Reset the cooldown
            self.player.current_tick_wait = self.player.ticks_per_move
        else:
            self.player.current_tick_wait -= 1

        # --- Handle Ghosts ---
        # for ghost in self.ghosts:
        #     if ghost.current_tick_wait <= 0:
        #         self._resolve_ghost_movement(ghost)
        #         ghost.current_tick_wait = ghost.ticks_per_move
        #     else:
        #         ghost.current_tick_wait -= 1

        # --- Post-movement checks ---
        self._consume_items()

    def _resolve_player_movement(self) -> None:
        """
        Applies automatic continuous movement and buffered inputs.
        """
        current_cell = self.maze.grid[self.player.y][self.player.x]

        # 1. Try to turn into the requested buffered direction
        if self._is_path_clear(current_cell, self.player.next_dir):
            self.player.current_dir = self.player.next_dir
            self._move_entity(self.player, self.player.current_dir)

        # 2. If turning is impossible, try to keep going straight automatically
        elif self._is_path_clear(current_cell, self.player.current_dir):
            self._move_entity(self.player, self.player.current_dir)

        # 3. Hit a wall, stop completely
        else:
            self.player.current_dir = "NONE"

    def _is_path_clear(self, cell, direction: str) -> bool:
        """
        Checks if the movement is blocked by a wall in the given direction.
        """
        if direction == "NONE":
            return False

        mapper = {"UP": "N", "DOWN": "S", "LEFT": "W", "RIGHT": "E"}
        # Remember: cell.wall[dir] is True if there IS a wall
        return not cell.wall[mapper[direction]]

    def _move_entity(self, entity: Player | Ghost, direction: str) -> None:
        """
        Updates the grid coordinates of an entity based on direction.
        """
        if direction == "UP":
            entity.y -= 1
        elif direction == "DOWN":
            entity.y += 1
        elif direction == "LEFT":
            entity.x -= 1
        elif direction == "RIGHT":
            entity.x += 1

    def _consume_items(self) -> None:
        """
        Handles score calculation and removes pacgums from the maze.
        """
        cell = self.maze.grid[self.player.y][self.player.x]

        # We assume subject points for pacgums are 10 and 50 respectively
        if cell.pacgum:
            self.player.score += 10
            cell.pacgum = False
        elif cell.super_pacgum:
            self.player.score += 50
            cell.super_pacgum = False
