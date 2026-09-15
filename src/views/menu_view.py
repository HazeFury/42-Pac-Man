import pygame

from ui.button import Button
from utils import game_config
from views.base_view import BaseView


class MenuView(BaseView):
    """
    The main menu view displaying the title and a start button.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        # Instantiate our custom button
        self.play_button = Button(
            pos_y="center",
            pos_x="center",
            text="START GAME",
            func=self.start_game,
            color="BLUE",
            size="large",
        )

    def start_game(self) -> None:
        """Callback function assigned to the play button."""
        print("Play button clicked! Transitioning to GAME state.")
        self.next_view = "GAME"

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            # The button handles its own click detection!
            self.play_button.handle_event(event)

    def update(self) -> None:
        # No specific background logic to update in the menu for now
        pass

    def draw(self) -> None:
        self.screen.fill(game_config.BACKGROUND_COLOR)

        # The button draws itself and handles its hover state!
        self.play_button.draw(self.screen)
