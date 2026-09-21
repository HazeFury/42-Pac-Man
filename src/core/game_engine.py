import sys

import pygame

from core.ghost import Ghost
from core.maze import Maze, Cell
from core.player import Player
from utils.input_manager import InputManager
from utils.parsing import Setup
from collections import deque


class GameEngine:
    """
    The core logic controller (Model).
    Manages the grid, entities, score, collisions, and the tick-based timeline.
    """

    def __init__(self, level_seed: int = 42) -> None:
        if len(sys.argv) > 1:
            config = Setup.from_json_file()
        else:
            config = Setup()
        self.clock = pygame.time.Clock()
        self.maze = Maze(
            seed=config.seed,
            w=config.width,
            h=config.height,
            pacgum=config.pacgum,
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

        # Tick timer management
        self.tick_timer: float = 0.0
        # Reduced to 0.25s for a more playable Pac-Man speed
        self.tick_threshold: float = 0.2

        self.is_game_over: bool = False

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
        if self.is_game_over:
            return

        self.tick_timer += dt
        if self.tick_timer >= self.tick_threshold:
            self._tick()
            self.tick_timer -= self.tick_threshold
        self.pacman_vs_ghost()
        if self.player.lives == 0:
            print("game over man")

        self.level_end()

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

        self.ghost_ai()

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

    def _is_path_clear(self, cell: Cell, direction: str) -> bool:
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

    def pacman_vs_ghost(self) -> None:
        p_x, p_y = self.player.x, self.player.y
        for ghost in self.ghosts:
            g_x, g_y = ghost.x, ghost.y
            if p_x == g_x and p_y == g_y:
                # if flagsuperpacgum
                self.player.lives -= 1
                self.nb_of_death += 1
                print(f"you died {self.nb_of_death} time")

    def level_end(self) -> None:
        count = 0
        for colum in self.maze.grid:
            for cell in colum:
                if cell.pacgum is True:
                    count += 1
        if count == 0:
            print("you win")

    def ghost_ai(self) -> None:
        moves = [(0, -1, 'N'), (1, 0, 'E'),
                 (0, 1, 'S'), (-1, 0, 'W')]
        maze = self.maze
        target_x, target_y = self.player.x, self.player.y
        for ghost in self.ghosts:
            start = (ghost.x, ghost.y)

            if ghost.ghost_type == "PINKY":
                target_x, target_y = self.player.x, self.player.y
                p_dir = self.player.current_dir
                if p_dir == "UP":
                    target_y = max(0, target_y - 2)
                elif p_dir == "DOWN":
                    target_y = min(maze.h - 1, target_y + 2)
                elif p_dir == "LEFT":
                    target_x = max(0, target_x - 2)
                elif p_dir == "RIGHT":
                    target_x = min(maze.w - 1, target_x + 2)

            if ghost.ghost_type == "INKY":
                target_x, target_y = self.player.x, self.player.y
                p_dir = self.player.current_dir
                g_x = self.ghosts[0].x
                g_y = self.ghosts[0].y
                pivot_x = target_x
                pivot_y = target_y
                if p_dir == "UP":
                    pivot_y = target_y - 2
                elif p_dir == "DOWN":
                    pivot_y = target_y + 2
                elif p_dir == "LEFT":
                    pivot_x = target_x - 2
                elif p_dir == "RIGHT":
                    pivot_x = target_x + 2
                raw_target_x = 2 * pivot_x - g_x
                raw_target_y = 2 * pivot_y - g_y
                target_x = max(0, min(maze.w - 1, raw_target_x))
                target_y = max(0, min(maze.h - 1, raw_target_y))

            if ghost.ghost_type == "CLYDE":
                target_x, target_y = self.player.x, self.player.y
                distance = (ghost.x - target_x) ** 2 + (ghost.y - target_y)**2
                if distance < 64:
                    target_x = 0
                    target_y = maze.h - 1

            end = (target_x, target_y)
            queue = deque([start])
            visited: dict[tuple[int, int],
                          tuple[int, int]] = {start: start}
            while queue:
                x, y = queue.popleft()
                for dx, dy, direction in moves:
                    nx = x + dx
                    ny = y + dy
                    if (0 <= nx < maze.w and 0 <= ny < maze.h
                        and not (maze.grid[y][x].wall[direction])
                            and (nx, ny) not in visited):
                        visited[(nx, ny)] = (x, y)
                        if (nx, ny) == end:
                            break
                        queue.append((nx, ny))
            if end in visited:
                curr: tuple[int, int] = end
                while visited[curr] != start:
                    curr = visited[curr]
                ghost.x, ghost.y = curr
