import pygame

from core.maze import Maze
from core.game_engine import GameEngine
from ui.button import Button
from ui.sprite import Sprite
from utils import game_config
from views.base_view import BaseView


class GameView(BaseView):
    """
    The main game view where the Pac-Man logic will happen.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.game_engin = GameEngine()
        self.pacman = self.game_engin.player

        # Assuming you load your images somewhere in your initialization
        # This dictionary maps the wall direction to the loaded Pygame Surface
        self.WALL_SPRITES = {
            "N": pygame.image.load("assets/walls/top.png").convert_alpha(),
            "S": pygame.image.load("assets/walls/bottom.png").convert_alpha(),
            "E": pygame.image.load("assets/walls/right.png").convert_alpha(),
            "W": pygame.image.load("assets/walls/left.png").convert_alpha(),
            "F": pygame.image.load("assets/walls/fix.png").convert_alpha(),
        }

        self.PACGUM_SPRITE = pygame.image.load(
            "assets/other/dot.png"
        ).convert_alpha()
        self.SUPER_PACGUM_SPRITE = pygame.image.load(
            "assets/other/apple.png"
        ).convert_alpha()

        self.back_button = Button(
            pos_y="top",
            pos_x="left",
            text="BACK",
            func=self.go_back,
            color="RED",
            size="small",
        )
        x_offset, y_offset = self.maze_centering()

        self.player_x: int = self.game_engin.maze.grid[self.pacman.y][self.pacman.x].x * \
            32 + x_offset + 9
        self.player_y: int = self.game_engin.maze.grid[self.pacman.y][self.pacman.x].y * \
            32 + y_offset + 8
        self.player_speed: int = 4

        # Using kwargs (pos_y=..., pos_x=...) prevents mixing up coordinates!
        self.pacman_sprite = Sprite(
            pos_y=self.player_y,
            pos_x=self.player_x,
            image_paths=[
                "assets/pacman-up/1.png",
                "assets/pacman-up/2.png",
                "assets/pacman-up/3.png",
                "assets/pacman-up/2.png",
            ],
            animation_speed=0.1,
        )

    def go_back(self) -> None:
        """Callback to return to the menu."""
        self.next_view = "MENU"

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            self.back_button.handle_event(event)

    def update(self, dt: float = 0.012) -> None:
        """
        Update the game logic.
        dt (delta_time) is the elapsed time in seconds since the last frame.
        """
        # 1. Update the animation properly with a realistic delta time
        self.pacman_sprite.update_animation(dt)

        keys = pygame.key.get_pressed()

        # 2. Update the actual variables tracking the player's position
        if keys[pygame.K_UP]:
            self.player_y -= self.player_speed
        if keys[pygame.K_DOWN]:
            self.player_y += self.player_speed
        if keys[pygame.K_LEFT]:
            self.player_x -= self.player_speed
        if keys[pygame.K_RIGHT]:
            self.player_x += self.player_speed

        # 3. Apply the new variables to the sprite's position
        self.pacman_sprite.update_position(self.player_x, self.player_y)

    def draw_maze(self, screen: pygame.Surface, cell_size: int = 32) -> None:
        """
        Iterates through the maze grid and draws walls and items.
        cell_size is the dimension of one square cell in pixels.
        """
        x_offset, y_offset = self.maze_centering()
        for row in self.game_engin.maze.grid:
            for cell in row:
                # 1. Calculate absolute pixel coordinates for the top-left
                # corner of the cell
                px_x = cell.x * cell_size + x_offset
                px_y = cell.y * cell_size + y_offset

                # 2. Draw walls based on the boolean dictionary
                if cell.wall["N"]:
                    screen.blit(self.WALL_SPRITES["N"], (px_x, px_y))
                # if cell.wall["S"]:
                #     screen.blit(self.WALL_SPRITES["S"], (px_x, px_y))
                # if cell.wall["E"]:
                #     screen.blit(self.WALL_SPRITES["E"], (px_x, px_y))
                if cell.wall["W"]:
                    screen.blit(self.WALL_SPRITES["W"], (px_x, px_y))

                if cell.x == self.game_engin.maze.w - 1:
                    screen.blit(self.WALL_SPRITES["E"], (px_x, px_y))
                if cell.y == self.game_engin.maze.h - 1:
                    screen.blit(self.WALL_SPRITES["S"], (px_x, px_y))
                if (
                    self.game_engin.maze.grid[(cell.y - 1)][cell.x].wall["W"]
                    and self.game_engin.maze.grid[cell.y][cell.x - 1].wall["N"]
                ):
                    screen.blit(self.WALL_SPRITES["F"], (px_x, px_y))

                    # 3. Draw consumables in the center of the cell
                if cell.super_pacgum:
                    # You might need an offset here to perfectly center
                    #  the pacgum sprite
                    screen.blit(
                        self.SUPER_PACGUM_SPRITE, (px_x + 10, px_y + 10)
                    )
                elif cell.pacgum:
                    screen.blit(self.PACGUM_SPRITE, (px_x + 11, px_y + 11))

    def maze_centering(self) -> tuple[int, int]:
        maze_pixel_w = self.game_engin.maze.w * 32
        maze_pixel_h = self.game_engin.maze.h * 32
        x_offset = (game_config.WINDOW_WIDTH - maze_pixel_w) // 2
        y_offset = (game_config.WINDOW_HEIGHT - maze_pixel_h) // 2
        return (x_offset, y_offset)

    def draw(self) -> None:
        self.screen.fill(game_config.BLACK)
        self.back_button.draw(self.screen)
        self.pacman_sprite.draw(self.screen)
        self.draw_maze(self.screen)
