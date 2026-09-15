import sys

import pygame

from ui.box import Box
from ui.button import Button
from ui.text import Text
from utils import game_config
from views.base_view import BaseView


class MenuView(BaseView):
    """
    The main menu view displaying the title and a start button.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        self.menu_box = Box(pos_y="center", pos_x="center", spacing=30)

        self.title_text = Text(
            pos_y="0",
            pos_x="0",
            text="PAC MAN",
            color="YELLOW",
            font_size=80,
        )
        self.play_btn = Button(
            pos_y="0",
            pos_x="0",
            text="START GAME",
            func=self.start_game,
            color="BLUE",
        )
        self.quit_btn = Button(
            pos_y="0", pos_x="0", text="QUIT", func=self.exit_game, color="RED"
        )

        # We add them to the box. The pos_y and pos_x of the elements are
        # ignored and overwritten by the Box layout logic!
        self.menu_box.add_child(self.title_text)
        self.menu_box.add_child(self.play_btn)
        self.menu_box.add_child(self.quit_btn)

    def start_game(self) -> None:
        """Callback function assigned to the play button."""
        self.next_view = "GAME"

    def exit_game(self) -> None:
        """Callback function assigned to the play button."""
        pygame.quit()
        sys.exit()

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            self.menu_box.handle_event(event)

    def update(self) -> None:
        # No specific background logic to update in the menu for now
        pass

    def draw(self) -> None:
        self.screen.fill(game_config.BACKGROUND_COLOR)
        self.menu_box.draw(self.screen)
