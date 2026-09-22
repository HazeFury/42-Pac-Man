import pygame

from ui.box import Box
from ui.button import Button
from ui.text import Text
from utils import game_config
from views.base_view import BaseView


class EndGameView(BaseView):
    """
    The main menu view displaying the title and a start button.
    """

    def __init__(self, screen: pygame.Surface, is_victory: bool) -> None:
        super().__init__(screen)

        self.menu_box = Box(pos_y="center", pos_x="center", spacing=60)

        end_msg = "VICTORY" if is_victory is True else "GAME OVER"

        self.menu_box.add_child(
            Text(
                pos_y="0",
                pos_x="0",
                text=f"{end_msg}",
                color=f"{'GREEN' if is_victory is True else 'RED'}",
                font_size=96,
            )
        )

        if is_victory is True:
            self.menu_box.add_child(
                Text(
                    pos_y="0",
                    pos_x="0",
                    text="Congrats !! You win this level :)",
                    color="WHITE",
                    font_size=48,
                )
            )

        self.menu_box.add_child(
            Button(
                pos_y="0",
                pos_x="0",
                text="Go back to menu",
                func=self.return_to_menu,
                color="RED",
            )
        )

    def return_to_menu(self) -> None:
        """Callback function assigned to the play button."""
        self.next_view = "MENU"

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            self.menu_box.handle_event(event)

    def update(self) -> None:
        # No specific background logic to update in the menu for now
        pass

    def draw(self) -> None:
        self.screen.fill(game_config.BACKGROUND_COLOR)
        self.menu_box.draw(self.screen)
