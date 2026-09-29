import pygame

from ui.box import Box
from ui.button import Button
from ui.text import Text
from utils import game_config
from views.base_view import BaseView


class RulesView(BaseView):
    """
    The main menu view displaying the title and a start button.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.instruct_box = Box(pos_y="center", pos_x="center", spacing=20)

        self.exit_btn = Button(
            pos_y="top",
            pos_x="left",
            text="Back",
            func=self.return_to_home,
            color="RED",
        )

        # Toutes les instructions ici
        self.instruct_box.add_child(
            Text(
                pos_y="0",
                pos_x="center",
                text="HOW TO PLAY",
                color="GREEN",
                font_size=96,
            )
        )

        instructions = [
            (
                "GOAL",
                "Eat all the small dots in the maze to complete the level.",
                "VIOLET",
            ),
            (
                "CONTROLS",
                "Use Arrow Keys or Z, Q, S, D to move Pac-Man.",
                "YELLOW",
            ),
            (
                "GHOSTS",
                "Avoid them! If a ghost catches you, you lose a life.",
                "RED",
            ),
            (
                "ENERGIZERS",
                "Eat fruits in the corners to make ghosts edible temporarily.",
                "BLUE",
            ),
            ("PAUSE", "Press ESC to pause the game at any time.", "ORANGE"),
            (
                "CHEATS",
                "F1: God Mode | F2: Freeze Ghosts | F3: Speed Boost | "
                "F4: +1 Life | F5: Skip Level",
                "VIOLET",
            ),
        ]

        for title, desc, color in instructions:
            self.instruct_box.add_child(
                Text(
                    pos_y="0",
                    pos_x="center",
                    text=title,
                    color=color,
                    font_size=64,
                )
            )
            self.instruct_box.add_child(
                Text(
                    pos_y="0",
                    pos_x="center",
                    text=desc,
                    color="WHITE",
                    font_size=48,
                )
            )

    def return_to_home(self) -> None:
        """Callback function assigned to the play button."""
        self.next_view = "MENU"

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            self.exit_btn.handle_event(event)

    def update(self) -> None:
        # No specific background logic to update in the menu for now
        pass

    def draw(self) -> None:
        self.screen.fill(game_config.BACKGROUND_COLOR)
        self.exit_btn.draw(self.screen)
        self.instruct_box.draw(self.screen)
