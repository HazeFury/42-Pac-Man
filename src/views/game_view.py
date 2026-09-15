import pygame

from ui.button import Button
from utils import game_config
from views.base_view import BaseView


class GameView(BaseView):
    """
    The main game view where the Pac-Man logic will happen.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        # A simple back button to test the view switching
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
        self.player_size: int = 20
        self.player_speed: int = 4

    def go_back(self) -> None:
        """Callback to return to the menu."""
        self.next_view = "MENU"

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            self.back_button.handle_event(event)

    def update(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player_y -= self.player_speed
        if keys[pygame.K_DOWN]:
            self.player_y += self.player_speed
        if keys[pygame.K_LEFT]:
            self.player_x -= self.player_speed
        if keys[pygame.K_RIGHT]:
            self.player_x += self.player_speed

    def draw(self) -> None:
        self.screen.fill(game_config.BLACK)
        self.back_button.draw(self.screen)

        # Just drawing a placeholder for the game
        pygame.draw.circle(
            self.screen,
            game_config.YELLOW,
            (self.player_x, self.player_y),
            self.player_size,
        )
