import sys

import pygame

from core.ghost import Ghost
from core.maze import Cell, Maze
from core.player import Player
from utils.input_manager import InputManager
from utils.parsing import config


class GameEngine:
    """
    The core logic controller (Model).
    Manages the grid, entities, score, collisions, and the tick-based timeline.
    """

    def __init__(self, level_seed: int = 42) -> None:
        if len(sys.argv) > 1:
            self.config = config.from_json_file()
        else:
            self.config = config
        self.clock = pygame.time.Clock()
        self.maze = Maze(
            seed=self.config.seed,
            w=self.config.width,
            h=self.config.height,
            pacgum=self.config.pacgum,
        )
        self.player = Player(
            start_x=(
                (self.maze.w // 2)
                if (self.maze.w % 2) != 0
                else ((self.maze.w // 2) - 1)
            ),
            start_y=self.maze.h // 2,
        )
        self.ghosts: list[Ghost] = [
            Ghost(start_x=0, start_y=0, ghost_type="BLINKY"),
            Ghost(start_x=self.maze.w - 1, start_y=0, ghost_type="PINKY"),
            Ghost(start_x=0, start_y=self.maze.h - 1, ghost_type="INKY"),
            Ghost(
                start_x=self.maze.w - 1,
                start_y=self.maze.h - 1,
                ghost_type="CLYDE",
            ),
        ]
        self.input_manager = InputManager()
        self.nb_of_death = 0
        self.is_game_over: bool = False

        # Tick timer management
        self.tick_timer: float = 0.0
        # Reduced to 0.25s for a more playable Pac-Man speed
        self.tick_threshold: float = 0.2

    def handle_input(self) -> None:
        """
        Receives input from the Controller/View and queues it.
        """
        direction: str = self.input_manager.get_movement_intention()
        self.player.queue_direction(direction)

    def update(self) -> None:
        """
        Accumulates delta time and triggers a game tick when the
        threshold is met.
        """
        raw_dt = self.clock.tick() / 1000.0
        dt = min(raw_dt, 0.1)

        if self.player.update(dt):
            self._resolve_player_movement()
        for ghost in self.ghosts:
            if ghost.update_position(dt):
                ghost.ghost_ai(
                    self.maze,
                    self.player.x,
                    self.player.y,
                    self.ghosts[0],
                    self.player.next_dir,
                )

        self.pacman_vs_ghost()
        self._consume_items()
        if self.player.lives == 0:
            print("game over man")
        self.level_end()

    def _resolve_player_movement(self) -> None:
        """
        Applies automatic continuous movement and buffered inputs.
        """
        current_cell = self.maze.grid[self.player.y][self.player.x]

        # 1. Try to turn into the requested buffered direction
        if self._is_path_clear(current_cell, self.player.next_dir):
            self.player.current_dir = self.player.next_dir
            self.player.next_move(self.player.next_dir)

        # 2. If turning is impossible, try to keep going straight automatically
        elif self._is_path_clear(current_cell, self.player.current_dir):
            self.player.next_move(self.player.current_dir)

        # 3. Hit a wall, stop completely
        else:
            self.player.current_dir = "NONE"

    def _is_path_clear(self, cell: Cell, direction: str) -> bool:
        """
        Checks if the movement is blocked by a wall in the given direction.
        """
        if direction == "NONE":
            return False
        mapper = {"UP": "N", "DOWN": "S", "LEFT": "W", "RIGHT": "E"}
        # Remember: cell.wall[dir] is True if there IS a wall
        return not cell.wall[mapper[direction]]

    def _consume_items(self) -> None:
        """
        Handles score calculation and removes pacgums from the maze.
        """
        cell = self.maze.grid[self.player.y][self.player.x]

        # We assume subject points for pacgums are 10 and 50 respectively
        if cell.pacgum:
            self.player.add_score(self.config.points_per_pacgum)
            cell.pacgum = False
        elif cell.super_pacgum:
            self.player.add_score(self.config.points_per_super_pacgum)
            cell.super_pacgum = False

    def pacman_vs_ghost(self) -> None:
        p_x, p_y = self.player.x, self.player.y
        for ghost in self.ghosts:
            g_x, g_y = ghost.x, ghost.y
            if p_x == g_x and p_y == g_y:
                # if flagsuperpacgum
                self.player.lives -= 1
                self.nb_of_death += 1
                # print(f"you died {self.nb_of_death} time")

    def level_end(self) -> None:
        count = 0
        for colum in self.maze.grid:
            for cell in colum:
                if cell.pacgum is True:
                    count += 1
        if count == 0:
            print("you win")

    def get_player_score(self) -> int:
        return self.player.score
