import random
from collections import deque
from src.core.maze import Maze


class Ghost:
    """
    Represents a ghost enemy in the maze.

    Tracks its position, spawn point, type, and current state.
    """

    def __init__(self, ghost_type: str) -> None:
        """
        Initialize the ghost with its spawn position and type.
        """
        self.x: int = 0
        self.y: int = 0
        self.prev_x: float = self.x
        self.prev_y: float = self.y

        # Spawn coordinates to return to when eaten
        self.spawn_x: int = self.x
        self.spawn_y: int = self.y

        # "BLINKY", "PINKY", "INKY", "CLYDE"
        self.ghost_type: str = ghost_type
        self.clyde_is_fleeing: bool = False

        # Speed expressed in engine ticks required to move
        self.move_delay: float = 0.5
        self.timer: float = 0
        self.respawn_timer: float = 0
        self.respawn_cooldown = 2

        # States could be: "CHASE", "FRIGHTENED", "DEAD"
        self.state: str = "CHASE"
        self.direction: str = "STOP"

    def update_position(self, dt: float) -> bool:
        """
        Update the movement and respawn timers.

        Returns True if the ghost is ready to move, False otherwise.
        """
        self.respawn(dt)
        if self.state == "DEAD":
            return False

        self.timer += dt
        if self.timer >= self.move_delay:
            self.timer -= self.move_delay
            return True

        return False

    def get_visual_pos(self) -> tuple[float, float]:
        """
        Returns interpolated (x, y) coordinates between previous and current
        tile positions for 60+ FPS smooth rendering.
        """
        if self.state == "DEAD":
            return (float(self.x), float(self.y))

        if self.move_delay > 0:
            progress = min(1.0, max(0.0, self.timer / self.move_delay))
        else:
            progress = 1.0
        vis_x = self.prev_x + (self.x - self.prev_x) * progress
        vis_y = self.prev_y + (self.y - self.prev_y) * progress
        return (vis_x, vis_y)

    def respawn(self, dt: float) -> bool:
        """
        Handle the respawn timer when the ghost is dead.

        Returns True when the ghost respawns, False otherwise.
        """
        if self.state == "DEAD":
            self.respawn_timer += dt
            if self.respawn_timer >= self.respawn_cooldown:
                self.state = "CHASE"
                self.respawn_timer = 0
                self.reset_position()
                return True
        return False

    def spawn(self, w: int, h: int) -> None:
        """Set corner spawn and visual coordinates according to ghost type."""
        if self.ghost_type == "BLINKY":
            self.spawn_x, self.spawn_y = 0, 0
        elif self.ghost_type == "PINKY":
            self.spawn_x, self.spawn_y = w - 1, 0
        elif self.ghost_type == "INKY":
            self.spawn_x, self.spawn_y = 0, h - 1
        elif self.ghost_type == "CLYDE":
            self.spawn_x, self.spawn_y = w - 1, h - 1
        self.x, self.y = self.spawn_x, self.spawn_y
        self.prev_x, self.prev_y = self.x, self.y
        self.timer = 0.0

    def reset_position(self) -> None:
        """
        Reset the ghost back to its initial spawn position.
        """
        self.x, self.y = self.spawn_x, self.spawn_y
        self.prev_x, self.prev_y = self.x, self.y
        self.timer = 0.0

    def ghost_ai(self, maze: Maze, pacman_x: int, pacman_y: int,
                 blinky: "Ghost", pacman_dir: str) -> None:
        """
        Execute ghost decision-making: flee if frightened,
         otherwise pathfind to target.
        """
        if self.state == "DEAD":
            return
        # 1. Frightened state: random flee movement
        if self.state == "FRIGHTENED":
            self._move_frightened(maze, pacman_x, pacman_y)
            return
        # 2. Chase state: compute personality target
        target = self._get_chase_target(
            maze, pacman_x, pacman_y, pacman_dir, blinky)
        # 3. Pathfinding: compute next step via BFS
        next_step = self._bfs_next_step(
            maze, target, fallback=(
                pacman_x, pacman_y))

        self.prev_x, self.prev_y = self.x, self.y
        self.x, self.y = next_step

    def _get_chase_target(
        self,
        maze: Maze,
        pacman_x: int,
        pacman_y: int,
        pacman_dir: str,
        blinky: "Ghost",
    ) -> tuple[int, int]:
        """
        Calculate target tile based on individual ghost personality:
        - BLINKY: Aggressive, directly targets Pac-Man.
        - PINKY: Ambush, targets 2 tiles ahead of Pac-Man.
        - INKY: Flanker, mirrors Blinky's vector across pivot.
        - CLYDE: Cowardly, chases if far, flees to corner if close.
        """
        offsets = {
            "UP": (0, -2),
            "DOWN": (0, 2),
            "LEFT": (-2, 0),
            "RIGHT": (2, 0),
        }
        dx, dy = offsets.get(pacman_dir, (0, 0))

        # BLINKY: Direct chase
        if self.ghost_type == "BLINKY":
            return (pacman_x, pacman_y)

        # PINKY: Ambush 2 tiles ahead
        if self.ghost_type == "PINKY":
            return (
                max(0, min(maze.w - 1, pacman_x + dx)),
                max(0, min(maze.h - 1, pacman_y + dy)),
            )

        # INKY: Vector from Blinky to 2 tiles ahead
        if self.ghost_type == "INKY":
            pivot_x = pacman_x + dx
            pivot_y = pacman_y + dy
            raw_x = 2 * pivot_x - blinky.x
            raw_y = 2 * pivot_y - blinky.y
            return (
                max(0, min(maze.w - 1, raw_x)),
                max(0, min(maze.h - 1, raw_y)),
            )

        # CLYDE: Run away to bottom-right corner if closer than ~5.6 tiles
        if self.ghost_type == "CLYDE":
            dist_sq = (self.x - pacman_x) ** 2 + (self.y - pacman_y) ** 2
            if dist_sq < 32:
                self.clyde_is_fleeing = True
            elif dist_sq > 58:
                self.clyde_is_fleeing = False

            if self.clyde_is_fleeing:
                return (maze.w - 1, maze.h - 1)
            return (pacman_x, pacman_y)

        return (pacman_x, pacman_y)

    def _move_frightened(
        self, maze: Maze, pacman_x: int, pacman_y: int
    ) -> None:
        """
        Pick a valid neighbouring cell, prioritizing directions
        moving away from Pac-Man.
        """
        moves = [(0, -1, "N"), (1, 0, "E"), (0, 1, "S"), (-1, 0, "W")]
        curr_dist = (self.x - pacman_x) ** 2 + (self.y - pacman_y) ** 2
        possible_moves = []
        flee_moves = []

        for dx, dy, direction in moves:
            next_x, next_y = self.x + dx, self.y + dy
            if 0 <= next_x < maze.w and 0 <= next_y < maze.h:
                if not maze.grid[self.y][self.x].wall[direction]:
                    possible_moves.append((next_x, next_y))
                    if (
                        (next_x - pacman_x) ** 2 + (next_y - pacman_y) ** 2
                        > curr_dist
                    ):
                        flee_moves.append((next_x, next_y))

        chosen = random.choice(flee_moves) if flee_moves else (
            random.choice(possible_moves) if possible_moves else (
                self.x, self.y
            )
        )
        self.prev_x, self.prev_y = self.x, self.y
        self.x, self.y = chosen

    def _bfs_next_step(
        self, maze: Maze, target: tuple[int, int], fallback: tuple[int, int]
    ) -> tuple[int, int]:
        """
        Run Breadth-First Search (BFS) to find the immediate
        next step towards target.
        Falls back to Pac-Man position if target is
        inside a wall / unreachable.
        """
        start = (self.x, self.y)
        moves = [(0, -1, "N"), (1, 0, "E"), (0, 1, "S"), (-1, 0, "W")]
        queue = deque([start])
        visited: dict[tuple[int, int], tuple[int, int]] = {start: start}
        found = False

        while queue and not found:
            curr_x, curr_y = queue.popleft()
            for dx, dy, direction in moves:
                next_x = curr_x + dx
                next_y = curr_y + dy
                if (
                    0 <= next_x < maze.w
                    and 0 <= next_y < maze.h
                    and not maze.grid[curr_y][curr_x].wall[direction]
                    and (next_x, next_y) not in visited
                ):
                    visited[(next_x, next_y)] = (curr_x, curr_y)
                    if (next_x, next_y) == target:
                        found = True
                        break
                    queue.append((next_x, next_y))

        # Target unreachable or already there: fallback
        end = target
        if (end not in visited or end == start) and fallback in visited:
            end = fallback

        # Trace back to immediate next tile
        if end in visited and end != start:
            curr = end
            while visited[curr] != start:
                curr = visited[curr]
            return curr

        return (self.x, self.y)
