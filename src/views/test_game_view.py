import pygame

from ui.button import Button
from ui.sprite import Sprite
from utils import game_config
from views.base_view import BaseView


class TestGameView(BaseView):
    """
    The main game view where the Pac-Man logic will happen.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        self.back_button = Button(
            pos_y="top",
            pos_x="left",
            text="BACK",
            func=self.go_back,
            color="RED",
            size="small",
        )

        self.player_x: int = game_config.WINDOW_WIDTH // 2
        self.player_y: int = game_config.WINDOW_HEIGHT // 2
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

    def draw(self) -> None:
        self.screen.fill(game_config.BLACK)
        self.back_button.draw(self.screen)
        self.pacman_sprite.draw(self.screen)
