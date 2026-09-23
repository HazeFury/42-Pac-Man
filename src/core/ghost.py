import random
from collections import deque
from core.maze import Maze


class Ghost:
    """
    Represents a ghost enemy in the maze.

    Tracks its position, spawn point, type, and current state.
    """

    def __init__(self, start_x: int, start_y: int,
                 ghost_type: str) -> None:
        """
        Initialize the ghost with its spawn position and type.
        """
        # Grid coordinates
        self.x: int = start_x
        self.y: int = start_y

        # Spawn coordinates to return to when eaten
        self.spawn_x: int = start_x
        self.spawn_y: int = start_y

        # "BLINKY", "PINKY", etc. Determines the AI behavior
        self.ghost_type: str = ghost_type

        # Speed expressed in engine ticks required to move
        self.move_delay: float = 0.3
        self.timer: float = 0
        self.respawn_timer = 0
        self.respawn_cooldown = 2

        # States could be: "CHASE", "SCATTER", "FRIGHTENED", "DEAD"
        self.state: str = "CHASE"
        self.direction: str = "STOP"

    def update_position(self, dt: float) -> bool:
        """
        Update the movement and respawn timers.

        Returns True if the ghost is ready to move, False otherwise.
        """
        self.respawn(dt)
        if self.state != "DEAD":
            self.timer += dt
            if self.timer >= self.move_delay:
                self.timer -= self.move_delay
                return True
            else:
                return False
        return False

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

    def change_state(self, new_state: str) -> None:
        """
        Change the current state of the ghost (e.g. CHASE, DEAD).
        """
        pass

    def reset_position(self) -> None:
        """
        Reset the ghost back to its initial spawn position.
        """
        self.x, self.y = self.spawn_x, self.spawn_y

    def calculate_next_move(self, target_x: int, target_y: int) -> None:
        """
        Calculate the next position towards the target coordinates.
        """
        pass

    def ghost_ai(self, map: Maze, x: int, y: int,
                 blinky: "Ghost", direction: str) -> None:
        """
        Find and move to the next cell using BFS pathfinding.

        Computes a target based on the ghost type and player position.
        """
        moves = [(0, -1, "N"), (1, 0, "E"), (0, 1, "S"), (-1, 0, "W")]
        maze = map
        target_x, target_y = x, y
        start = (self.x, self.y)
        if self.state == "CHASE":
            if self.ghost_type == "PINKY":
                target_x, target_y = x, y
                p_dir = direction
                if p_dir == "UP":
                    target_y = max(0, target_y - 2)
                elif p_dir == "DOWN":
                    target_y = min(maze.h - 1, target_y + 2)
                elif p_dir == "LEFT":
                    target_x = max(0, target_x - 2)
                elif p_dir == "RIGHT":
                    target_x = min(maze.w - 1, target_x + 2)
            if self.ghost_type == "INKY":
                target_x, target_y = x, y
                p_dir = direction
                g_x = blinky.x
                g_y = blinky.y
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
            if self.ghost_type == "CLYDE":
                target_x, target_y = x, y
                distance = (self.x - target_x) ** 2 + (
                    self.y - target_y
                ) ** 2
                if distance < 32:
                    target_x = 0
                    target_y = maze.h - 1
        if self.state == "FRIGHTENED":
            possible_moves = []
            current_dist = (self.x - x) ** 2 + (self.y - y) ** 2
            flee_moves = []
            for dx, dy, direction in moves:
                nx = self.x + dx
                ny = self.y + dy
                if 0 <= nx < maze.w and 0 <= ny < maze.h:
                    if not maze.grid[self.y][self.x].wall[direction]:
                        possible_moves.append((nx, ny))
                        new_dist = (nx - x) ** 2 + (ny - y) ** 2
                        if new_dist > current_dist:
                            flee_moves.append((nx, ny))
            if flee_moves:
                self.x, self.y = random.choice(flee_moves)
            elif possible_moves:
                self.x, self.y = random.choice(possible_moves)
            return

        end = (target_x, target_y)
        queue = deque([start])
        visited: dict[tuple[int, int], tuple[int, int]] = {start: start}
        while queue:
            cx, cy = queue.popleft()
            for dx, dy, direction in moves:
                nx = cx + dx
                ny = cy + dy
                if (
                    0 <= nx < maze.w
                    and 0 <= ny < maze.h
                    and not (maze.grid[cy][cx].wall[direction])
                    and (nx, ny) not in visited
                ):
                    visited[(nx, ny)] = (cx, cy)
                    if (nx, ny) == end:
                        break
                    queue.append((nx, ny))
        if end in visited:
            curr: tuple[int, int] = end
            while visited[curr] != start:
                curr = visited[curr]
            self.x, self.y = curr
