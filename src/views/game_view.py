import pygame

from core.game_engine import GameEngine
from core.ghost import Ghost
from ui.box import Box
from ui.button import Button
from ui.sprite import Sprite
from ui.text import Text
from utils import game_config
from views.base_view import BaseView


class GameView(BaseView):
    """
    The main game view where the Pac-Man logic will happen.
    """

    def __init__(
        self, screen: pygame.Surface, game_engine: GameEngine
    ) -> None:
        super().__init__(screen)
        self.game_engine = game_engine
        self.pacman = self.game_engine.player
        self.ghost = self.game_engine.ghosts

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

        self.data_box = Box(
            pos_y="top", pos_x="right", spacing=30, layout="horizontal"
        )

        self.back_button = Button(
            pos_y="top",
            pos_x="left",
            text="BACK",
            func=self.go_back,
            color="RED",
            size="small",
        )

        self.level_txt = Text(
            pos_y="top",
            pos_x="center",
            text=f"LEVEL : {str(self.game_engine.curr_level)}",
            color="WHITE",
        )

        self.life_txt = Text(
            pos_y="0",
            pos_x="0",
            text=f"LIFE : {str(self.game_engine.player.lives)}",
            color="WHITE",
        )

        self.time_txt = Text(
            pos_y="0",
            pos_x="0",
            text=f"TIME : {str(self.game_engine.countdown)}",
            color=f"{'RED' if self.game_engine.countdown < 10 else 'WHITE'}",
        )

        self.score_txt = Text(
            pos_y="0",
            pos_x="0",
            text=f"SCORE : {str(self.pacman.score)}",
            color="GREEN",
        )

        self.data_box.add_child(self.life_txt)
        self.data_box.add_child(self.time_txt)
        self.data_box.add_child(self.score_txt)

        x_offset, y_offset = self.maze_centering()

        self.player_x: int = self.pacman.x * 32 + x_offset + 9
        self.player_y: int = self.pacman.y * 32 + y_offset + 8

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
        ghost_assets = {
            "BLINKY": "assets/ghosts/blinky.png",
            "PINKY": "assets/ghosts/pinky.png",
            "INKY": "assets/ghosts/inky.png",
            "CLYDE": "assets/ghosts/clyde.png",
            "FRIGHTENED": "assets/ghosts/blue_ghost.png",
        }
        self.ghost_sprite: list[tuple[Ghost, Sprite, Sprite]] = []
        for ghost in self.game_engine.ghosts:
            normal_sprite = Sprite(
                pos_y=ghost.y * 32 + y_offset + 8,
                pos_x=ghost.x * 32 + x_offset + 9,
                image_paths=[ghost_assets[ghost.ghost_type]],
                animation_speed=0.1,
            )
            frightened_sprite = Sprite(
                pos_y=ghost.y * 32 + y_offset + 8,
                pos_x=ghost.x * 32 + x_offset + 9,
                image_paths=[ghost_assets["FRIGHTENED"]],
                animation_speed=0.1,
            )
            self.ghost_sprite.append((ghost, normal_sprite, frightened_sprite))

    def go_back(self) -> None:
        """Callback to return to the menu."""
        self.next_view = "MENU"

    def go_to_win_screen(self) -> None:
        """Callback to go to win screen."""
        self.next_view = "WIN"

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """
        Process standard UI events (like button clicks).
        Continuous keyboard state is handled in update().
        """
        for event in events:
            self.back_button.handle_event(event)

    def update(self, dt: float = 0.024) -> None:
        """
        Acts as a bridge between the user inputs, the Game Engine, and the
        visual Sprites.
        """
        # 1. the Engine capture user inputs (via the Controller Manager)
        self.game_engine.handle_input()

        # 2. Let the Engine resolve all the logic and ticks (The Model part)
        self.game_engine.update()

        # 3. Synchronize visuals with the Engine's truth (The View part)
        self.pacman_sprite.update_animation(dt)

        # Calculate new pixel position based on grid coordinates
        x_offset, y_offset = self.maze_centering()
        px = self.pacman.x * 32 + x_offset + 9
        py = self.pacman.y * 32 + y_offset + 8
        self.pacman_sprite.update_position(px, py)
        for ghost, normal_sprite, frightened_sprite in self.ghost_sprite:
            pos_y = ghost.y * 32 + y_offset + 8
            pos_x = ghost.x * 32 + x_offset + 9
            normal_sprite.update_position(pos_x, pos_y)
            frightened_sprite.update_position(pos_x, pos_y)

        # Update the UI data
        self.level_txt.update_text(
            f"LEVEL : {str(self.game_engine.curr_level)}"
        )
        self.score_txt.update_text(f"SCORE : {str(self.pacman.score)}")
        self.life_txt.update_text(
            f"LIFE : {str(self.game_engine.player.lives)}"
        )
        self.time_txt.update_text(
            f"TIME : {str(int(self.game_engine.countdown))}"
        )
        self.data_box.update_layout()

        if (
            self.game_engine.player.lives == 0
            or self.game_engine.countdown <= 0.0
        ):
            self.next_view = "GAMEOVER"
        elif (
            self.game_engine.level_end() is True
            and self.game_engine.curr_level == self.game_engine.total_levels
        ):
            self.next_view = "WIN"
        else:
            self.game_engine.check_is_game_finished()

    def draw_maze(self, screen: pygame.Surface, cell_size: int = 32) -> None:
        """
        Iterates through the maze grid and draws walls and items.
        cell_size is the dimension of one square cell in pixels.
        """
        x_offset, y_offset = self.maze_centering()
        for row in self.game_engine.maze.grid:
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

                if cell.x == self.game_engine.maze.w - 1:
                    screen.blit(self.WALL_SPRITES["E"], (px_x, px_y))
                if cell.y == self.game_engine.maze.h - 1:
                    screen.blit(self.WALL_SPRITES["S"], (px_x, px_y))
                if (
                    self.game_engine.maze.grid[(cell.y - 1)][cell.x].wall["W"]
                    and self.game_engine.maze.grid[cell.y][cell.x - 1].wall[
                        "N"
                    ]
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
        maze_pixel_w = self.game_engine.maze.w * 32
        maze_pixel_h = self.game_engine.maze.h * 32
        x_offset = (game_config.WINDOW_WIDTH - maze_pixel_w) // 2
        y_offset = (game_config.WINDOW_HEIGHT - maze_pixel_h) // 2
        return (x_offset, y_offset)

    def draw(self) -> None:
        self.screen.fill(game_config.BLACK)
        self.back_button.draw(self.screen)
        self.data_box.draw(self.screen)
        self.level_txt.draw(self.screen)
        self.draw_maze(self.screen)
        self.pacman_sprite.draw(self.screen)
        for ghost, normal_sprite, frightened_sprite in self.ghost_sprite:
            if ghost.state != "DEAD":
                if ghost.state == "FRIGHTENED":
                    frightened_sprite.draw(self.screen)
                else:
                    normal_sprite.draw(self.screen)
