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

    def __init__(self) -> None:

        self.clock = pygame.time.Clock()
        self.curr_level = 1
        self.lvl_cfg = config.get_level(self.curr_level)
        self.total_levels = config.get_amount_of_level()
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
        self.death = False
        self.is_game_over: bool = False
        self.super_pacgum = False
        self.super_pacgum_time = 0
        self.pause_timer: float = 1.0
        self.countdown = config.level_max_time

        from core.cheat_manager import CheatManager

        self.cheat_manager: CheatManager | None = None

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
        if self.pause_timer > 0:
            self.pause_timer -= dt
            return
        # Décrémentation du décompte
        if self.countdown > 0:
            self.countdown = max(0.0, self.countdown - dt)
            if self.countdown == 0:
                # Optionnel : déclencher la fin du niveau ou le game over
                # par manque de temps
                pass

        if self.player.update(dt):
            self._resolve_player_movement()

        if not (self.cheat_manager and self.cheat_manager.is_ghost_frozen):
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
        if self.super_pacgum:
            self.super_pacgum_timer(dt)

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
            self.player.add_score(config.points_per_pacgum)
            cell.pacgum = False
        elif cell.super_pacgum:
            self.player.add_score(config.points_per_super_pacgum)
            cell.super_pacgum = False
            self.super_pacgum = True
            for ghost in self.ghosts:
                if ghost.state != "DEAD":
                    ghost.state = "FRIGHTENED"

    def pacman_vs_ghost(self) -> None:
        p_x, p_y = self.player.x, self.player.y
        for ghost in self.ghosts:
            g_x, g_y = ghost.x, ghost.y
            if p_x == g_x and p_y == g_y:
                if ghost.state == "FRIGHTENED":
                    self.player.add_score(config.points_per_ghost)
                    ghost.state = "DEAD"
                elif ghost.state == "CHASE":
                    if self.cheat_manager and self.cheat_manager.is_invincible:
                        continue
                    self.player.lives -= 1
                    self.reset_position()
                    self.pause_timer = 1.0

    def level_end(self) -> bool:
        count = 0
        for colum in self.maze.grid:
            for cell in colum:
                if cell.pacgum is True:
                    count += 1
        if count == 0:
            return True
        else:
            return False

    def get_player_score(self) -> int:
        return self.player.score

    def reset_position(self) -> None:
        self.player.x, self.player.y = self.player.spawn_x, self.player.spawn_y
        for ghost in self.ghosts:
            ghost.x, ghost.y = ghost.spawn_x, ghost.spawn_y
        self.death = True

    def super_pacgum_timer(self, dt: float) -> None:
        if self.super_pacgum_time < 25:
            self.super_pacgum = True
            self.super_pacgum_time += dt
        else:
            self.super_pacgum = False
            self.super_pacgum_time = 0
            for ghost in self.ghosts:
                if ghost.state == "FRIGHTENED":
                    ghost.state = "CHASE"

    def check_is_game_finished(self) -> None:
        if self.level_end() is True and self.curr_level != self.total_levels:
            self.next_level()

    def next_level(self):
        self.curr_level += 1

        self.launch_new_game(is_from_menu=False)

    def launch_new_game(self, is_from_menu: bool) -> None:
        if is_from_menu is True:
            self.curr_level = 1
            self.player.score = 0
            self.player.lives = config.lives
            self.ghost_start_position()
            if self.cheat_manager:
                self.cheat_manager.is_invincible = False
                self.cheat_manager.is_ghost_frozen = False
                self.cheat_manager.is_speed_boosted = False

        self.lvl_cfg = config.get_level(self.curr_level)
        self.reset_position()
        self.maze.generate_maze(
            seed=self.lvl_cfg.seed,
            w=self.lvl_cfg.width,
            h=self.lvl_cfg.height,
            pacgum=self.lvl_cfg.pacgum,
        )
        self.ghost_start_position()
        self.countdown = config.level_max_time
        self.player.current_dir = "NONE"
        self.player.next_dir = "NONE"
        # self.player.respawn() ## pourquoi pas mettre ca pour pas le prochain
        # niveau commence tout de suite et qu'il y ai du délai

    def ghost_start_position(self):
        for ghost in self.ghosts:
            ghost.spawn(self.maze.w, self.maze.h)
            ghost.state = "CHASE"
        self.player.spawn(self.maze.w, self.maze.h)
