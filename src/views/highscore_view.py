import pygame

from ui.box import Box
from ui.button import Button
from ui.text import Text
from utils import game_config
from views.base_view import BaseView


class HighScoreView(BaseView):
    """
    The main menu view displaying the title and a start button.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        self.menu_box = Box(pos_y="center", pos_x="center", spacing=30)

        self.menu_box.add_child(
            Text(
                pos_y="0",
                pos_x="0",
                text="Top scorers",
                color="VIOLET",
                font_size=96,
            )
        )

        score_list = {
            "Marco": 98,
            "Guillaume": 86,
            "stmaire": 42,
            "Bruno": 852,
            "Yannick": 36,
            "Quentin": 72,
            "Cédric": 50,
            "Canelle": 1,
            "Matéo": 31,
            "Pierre": 65,
            "Jean": 57,
            "Pouet": 5,
        }

        self.sorted_score_list = dict(
            sorted(score_list.items(), key=lambda item: item[1], reverse=True)[
                :10
            ]
        )
        for name, score in self.sorted_score_list.items():
            self.menu_box.add_child(
                Text(
                    pos_y="0",
                    pos_x="0",
                    text=f"{name} : {score}",
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
                size="large",
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
