import pygame

from src.core.game_engine import GameEngine
from src.ui.box import Box
from src.ui.button import Button
from src.ui.input import TextInput
from src.ui.text import Text
from src.utils import game_config
from src.utils.highscore import HighScoreManager
from src.views.base_view import BaseView


class EndGameView(BaseView):
    """
    The end game view displaying game outcome and score submission.
    """

    def __init__(
        self, screen: pygame.Surface, game_engine: GameEngine, is_victory: bool
    ) -> None:
        """Initialize end game view with score display, inputs, and buttons."""
        super().__init__(screen)
        self.game_engine = game_engine
        self.score_manager = HighScoreManager()
        self.menu_box = Box(pos_y="center", pos_x="center", spacing=60)
        self.score: int = self.game_engine.get_player_score()

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

        self.score_str = Text(
            pos_y="0",
            pos_x="0",
            text=f"SCORE : {str(self.score)}",
            color="VIOLET",
            font_size=96,
        )

        self.menu_box.add_child(self.score_str)

        if is_victory is True:
            self.menu_box.add_child(
                Text(
                    pos_y="0",
                    pos_x="0",
                    text="Congrats !! You have completed all level :)",
                    color="BLUE",
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
                color="GREEN",
            )
        )

        self.menu_box.add_child(
            Button(
                pos_y="0",
                pos_x="0",
                text="Exit",
                func=self.return_to_menu,
                color="RED",
            )
        )

    def return_to_menu(self) -> None:
        """Callback function assigned to the go back button."""
        self.next_view = "MENU"

    def save_score(self) -> None:
        """Save the current score to the highscore.json file."""
        player_name = self.player_name_input.get_value()
        if len(player_name) >= 1:
            self.player_name_input.change_color(is_error=False)
            self.score_manager.write_highscore(player_name, self.score)
            self.next_view = "SCORE"
        else:
            self.player_name_input.change_color(is_error=True)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """Forward Pygame events to the end game UI box."""
        for event in events:
            self.menu_box.handle_event(event)

    def update(self) -> None:
        """Check for score changes and refresh the score display."""
        new_score: int = self.game_engine.get_player_score()

        if new_score != self.score:
            self.score = new_score
            self.score_str.update_text(f"SCORE : {str(self.score)}")

            self.menu_box.update_layout()

    def draw(self) -> None:
        """Render the background and end game UI components."""
        self.screen.fill(game_config.BACKGROUND_COLOR)
        self.menu_box.draw(self.screen)
