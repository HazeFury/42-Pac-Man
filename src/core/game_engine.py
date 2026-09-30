import pygame

from src.core.ghost import Ghost
from src.core.maze import Cell, Maze
from src.core.player import Player
from src.utils.input_manager import InputManager
from src.utils.parsing import config
from src.utils.random import get_random_int


class GameEngine:
    """
    The core logic controller (Model).
    Manages the grid, entities, score, collisions, and the tick-based timeline.
    """

    def __init__(self) -> None:
        """Initialize game state, maze, entities, and timers."""
        self.clock = pygame.time.Clock()
        self.curr_level: int = 1
        self.lvl_cfg = config.get_level(self.curr_level)
        self.total_levels = max(10, config.get_amount_of_level())
        self.maze = Maze()
        self.maze.generate_maze(
            seed=self.lvl_cfg.seed,
            w=self.lvl_cfg.width,
            h=self.lvl_cfg.height,
            pacgum=self.lvl_cfg.pacgum,
        )
        self.player = Player()

        self.ghosts: list[Ghost] = [
            Ghost(ghost_type="BLINKY"),
            Ghost(ghost_type="PINKY"),
            Ghost(ghost_type="INKY"),
            Ghost(
                ghost_type="CLYDE",
            ),
        ]

        self.input_manager = InputManager()
        self.super_pacgum = False
        self.super_pacgum_time: float = 0
        self.pause_timer: float = 1.0
        self.countdown: float = config.level_max_time
        self.death_collision_pause: float = 0

        from src.core.cheat_manager import CheatManager

        self.cheat_manager: CheatManager | None = None

        # Game lifecycle state: "PLAYING", "VICTORY",
        # "GAMEOVER"
        self.game_state: str = "PLAYING"

    def handle_input(self) -> None:
        """
        Receives input from the Controller/View and queues it.
        """
        direction: str = self.input_manager.get_movement_intention()
        self.player.queue_direction(direction)

    def update(self) -> None:
        """
        Accumulates delta time and triggers a game tick
        """
        raw_dt = self.clock.tick() / 1000.0
        dt = min(raw_dt, 0.1)

        # Handles both impact freeze and respawn pause
        if self._start_pause(dt):
            return

        if self.player.update(dt):
            self._resolve_player_movement()

        self._update_gameplay_timer(dt)

        self._update_ghosts(dt)
        self._consume_items()
        self._resolve_ghost_collisions()
        self._check_game_state()

    def _start_pause(self, dt: float) -> bool:
        """
        Handle all blocking pause states (hit impact and respawn countdown).
        Returns True if the engine tick should be skipped.
        """

        # Death impact freeze
        if self.death_collision_pause > 0:
            self.death_collision_pause -= dt
            if self.death_collision_pause <= 0:
                self.reset_position()
                self.pause_timer = 1.5
            return True

        # Respawn sequence
        if self.pause_timer > 0:
            self.update_respawn_delay(dt)
            return True

        return False

    def _update_gameplay_timer(self, dt: float) -> None:
        """
        Advance active gameplay clocks (level time limit
          and super pacgum duration).
        """

        if self.countdown > 0:
            self.countdown = max(0.0, self.countdown - dt)

        if self.super_pacgum:
            self.super_pacgum_timer(dt)

    def update_respawn_delay(self, dt: float) -> None:
        """
        Update the 1.5s respawn animation sequence.
        """
        self.pause_timer -= dt

        # Slide back to spawn
        if self.pause_timer > 1.0:
            self.player.timer = min(0.5, self.player.timer + dt)
            for ghost in self.ghosts:
                ghost.timer = min(ghost.move_delay, ghost.timer + dt)

        # Frozen on spawn waiting for go
        else:
            self.player.timer = 0.0
            self.player.prev_x = float(self.player.spawn_x)
            self.player.prev_y = float(self.player.spawn_y)
            for ghost in self.ghosts:
                ghost.timer = 0.0
                ghost.prev_x = float(ghost.spawn_x)
                ghost.prev_y = float(ghost.spawn_y)

        if self.pause_timer <= 0:
            self.player.timer = self.player.move_delay
            for ghost in self.ghosts:
                ghost.timer = ghost.move_delay

    def _resolve_player_movement(self) -> None:
        """
        Applies automatic continuous movement and buffered inputs.
        """
        self._consume_items()
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
            self.player.next_dir = "NONE"
            self.player.prev_x = self.player.x
            self.player.prev_y = self.player.y
            self.player.timer = self.player.move_delay

    def _update_ghosts(self, dt: float) -> None:
        """
        Process movement and AI pathfinding for each active ghost.
        Skipped if the ghost freeze cheat is active.
        """
        if self.cheat_manager and self.cheat_manager.is_ghost_frozen:
            return

        player_dir = (
            self.player.current_dir
            if self.player.current_dir != "NONE"
            else self.player.next_dir
        )
        for ghost in self.ghosts:
            if ghost.update_position(dt):
                ghost.ghost_ai(
                    self.maze,
                    self.player.x,
                    self.player.y,
                    self.ghosts[0],
                    player_dir,
                )

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
        p_vis_x, p_vis_y = self.player.get_visual_pos()
        dist_sq = (p_vis_x - cell.x) ** 2 + (p_vis_y - cell.y) ** 2

        if cell.pacgum:
            if dist_sq < 0.2:
                self.player.add_score(config.points_per_pacgum)
                cell.pacgum = False
                self.maze.total_pacgum -= 1
        elif cell.super_pacgum:
            if dist_sq < 0.2:
                self.player.add_score(config.points_per_super_pacgum)
                self.super_pacgum_time = 0
                cell.super_pacgum = False
                self.super_pacgum = True
                for ghost in self.ghosts:
                    if ghost.state != "DEAD":
                        ghost.state = "FRIGHTENED"

    def _resolve_ghost_collisions(self) -> None:
        """Handle visual collisions between Pac-Man and ghosts."""
        p_vis_x, p_vis_y = self.player.get_visual_pos()
        for ghost in self.ghosts:
            if ghost.state == "DEAD":
                continue
            g_vis_x, g_vis_y = ghost.get_visual_pos()
            dist_sq = (p_vis_x - g_vis_x) ** 2 + (p_vis_y - g_vis_y) ** 2
            if dist_sq < 0.1:
                if ghost.state == "FRIGHTENED":
                    self.player.add_score(config.points_per_ghost)
                    ghost.state = "DEAD"
                elif ghost.state == "CHASE":
                    if self.cheat_manager and self.cheat_manager.is_invincible:
                        continue
                    self.death_collision_pause = 0.8
                    self.player.lives -= 1
                    self.super_pacgum = False
                    self.super_pacgum_time = 0
                    for g in self.ghosts:
                        g.state = "CHASE"
                    break

    def get_player_score(self) -> int:
        """Return the player's current score."""
        return self.player.score

    def reset_position(self) -> None:
        """Reset Pac-Man and ghost coordinates to prepare their respawn."""
        self.player.prev_x, self.player.prev_y = self.player.get_visual_pos()
        self.player.x, self.player.y = self.player.spawn_x, self.player.spawn_y
        self.player.timer = 0.0
        self.player.current_dir = "NONE"
        self.player.next_dir = "NONE"
        for ghost in self.ghosts:
            ghost.prev_x, ghost.prev_y = ghost.get_visual_pos()
            ghost.x, ghost.y = ghost.spawn_x, ghost.spawn_y
            ghost.timer = 0.0

    def super_pacgum_timer(self, dt: float) -> None:
        """Update super pacgum duration and revert ghosts once expired."""
        if self.super_pacgum_time < 25:
            self.super_pacgum = True
            self.super_pacgum_time += dt
        else:
            self.super_pacgum = False
            self.super_pacgum_time = 0
            for ghost in self.ghosts:
                if ghost.state == "FRIGHTENED":
                    ghost.state = "CHASE"

    def launch_new_game(self, is_from_menu: bool) -> None:
        """Initialize state for a new game session or a subsequent level."""
        new_seed = get_random_int()
        if is_from_menu is True:
            new_seed = 42
            self.curr_level = 1
            self.player.score = 0
            self.pause_timer = 1
            self.player.lives = config.lives
            self.ghost_start_position()
            self.game_state = "PLAYING"
            if self.cheat_manager:
                self.cheat_manager.is_invincible = False
                self.cheat_manager.is_ghost_frozen = False
                self.cheat_manager.is_speed_boosted = False
                self.player.move_delay = self.cheat_manager.normal_move_delay

        self.lvl_cfg = config.get_level(self.curr_level)
        self.reset_position()
        self.pause_timer = 1
        self.maze.generate_maze(
            seed=new_seed,
            w=self.lvl_cfg.width,
            h=self.lvl_cfg.height,
            pacgum=self.lvl_cfg.pacgum,
        )
        self.ghost_start_position()
        self.countdown = config.level_max_time
        self.player.current_dir = "NONE"
        self.player.next_dir = "NONE"

    def ghost_start_position(self) -> None:
        """Reset ghosts and player to their initial maze spawn locations."""
        for ghost in self.ghosts:
            ghost.spawn(self.maze.w, self.maze.h)
            ghost.state = "CHASE"
        self.player.spawn(self.maze.w, self.maze.h)

    def _check_game_state(self) -> None:
        if self.level_end():
            if self.curr_level >= self.total_levels:
                self.game_state = "VICTORY"
            else:
                self.next_level()

        if self.countdown <= 0 or self.player.lives <= 0:
            self.game_state = "GAMEOVER"

    def level_end(self) -> bool:
        """Return True if all pacgums have been consumed."""
        if self.maze.total_pacgum == 0:
            return True
        else:
            return False

    def next_level(self) -> None:
        """Increment the level index and launch the new level."""
        self.curr_level += 1
        self.launch_new_game(is_from_menu=False)
