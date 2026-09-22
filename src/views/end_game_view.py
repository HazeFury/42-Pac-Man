import pygame

from ui.box import Box
from ui.button import Button
from ui.input import TextInput
from ui.text import Text
from utils import game_config
from utils.parsing import config
from views.base_view import BaseView


class EndGameView(BaseView):
    """
    The main menu view displaying the title and a start button.
    """

    def __init__(self, screen: pygame.Surface, is_victory: bool) -> None:
        super().__init__(screen)
        # self.game_engine = GameEngine()
        # if len(sys.argv) > 1:
        #     self.config = config.from_json_file()
        # else:
        #     self.config = config

        self.menu_box = Box(pos_y="center", pos_x="center", spacing=60)

        end_msg = "VICTORY" if is_victory is True else "GAME OVER"

        self.menu_box.add_child(
            Text(
                pos_y="0",
                pos_x="0",
                text=f"{end_msg}",
                color=f"{'GREEN' if is_victory is True else 'RED'}",
                font_size=192,
            )
        )

        if is_victory is True:
            self.menu_box.add_child(
                Text(
                    pos_y="0",
                    pos_x="0",
                    text="Congrats !! You win this level :)",
                    color="VIOLET",
                    font_size=96,
                )
            )

        self.menu_box.add_child(
            Text(
                pos_y="0",
                pos_x="0",
                text="Enter your name to save your score (max 10 char)",
                color="WHITE",
                font_size=32,
            )
        )

        self.player_name_input = TextInput(pos_x="0", pos_y="0")
        self.menu_box.add_child(self.player_name_input)

        self.menu_box.add_child(
            Button(
                pos_y="0",
                pos_x="0",
                text="Save score",
                func=self.save_score,
                color="RED",
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
        """Callback function assigned to the go back button."""
        self.next_view = "MENU"

    def go_to_score_view(self) -> None:
        """Callback function assigned to the save score button."""
        self.next_view = "SCORE"

    def save_score(self) -> None:
        """Save the current score to the highscore.json file."""
        score = self.game_engine.get_player_score()
        print(self.player_name_input.get_value())
        print(score)
        print(config.highscore_filename)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            self.menu_box.handle_event(event)

    def update(self) -> None:
        # No specific background logic to update in the menu for now
        pass

    def draw(self) -> None:
        self.screen.fill(game_config.BACKGROUND_COLOR)
        self.menu_box.draw(self.screen)
