import pygame

from ui.box import Box
from ui.button import Button
from ui.text import Text
from utils import game_config
from utils.highscore import HighScoreManager
from views.base_view import BaseView


class HighScoreView(BaseView):
    """
    The view displaying the top 10 scores dynamically.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        self.menu_box = Box(pos_y="center", pos_x="center", spacing=30)
        self.score_manager = HighScoreManager()
        self.scores = self.get_sorted_scores()

        # Build the UI for the first time
        self._build_ui()

    def _build_ui(self) -> None:
        """
        Clears the box and reconstructs all UI elements.
        Called on initialization and whenever the highscore data changes.
        """
        # 1. Empty the existing UI components
        self.menu_box.children.clear()

        # 2. Add the static title
        self.menu_box.add_child(
            Text(
                pos_y="0",
                pos_x="0",
                text="Top scorers",
                color="VIOLET",
                font_size=96,
            )
        )

        # 3. Generate new Text components based on the updated data
        for entry in self.scores:
            self.menu_box.add_child(
                Text(
                    pos_y="0",
                    pos_x="0",
                    text=f"{entry.name} : {entry.score}",
                    color="WHITE",
                    font_size=48,
                )
            )

        # 4. Add the back button
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

        # 5. Force the Box to calculate the layout for these new children
        self.menu_box.update_layout()

    def return_to_menu(self) -> None:
        """Callback function assigned to the back button."""
        self.next_view = "MENU"

    def get_sorted_scores(self) -> list:
        score_list = self.score_manager.read_highscore()
        result = self.sort_score_list(score_list.scores)
        return result

    def sort_score_list(self, score_list: list) -> list:
        valid_scores = [entry for entry in score_list if entry.name != ""]

        sorted_scores = sorted(
            valid_scores, key=lambda entry: entry.score, reverse=True
        )

        return sorted_scores[:10]

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            self.menu_box.handle_event(event)

    def update(self) -> None:
        """
        Checks for data changes. Rebuilds the UI if a new score was added.
        """
        new_score_list = self.get_sorted_scores()

        if self.scores != new_score_list:
            self.scores = new_score_list
            self._build_ui()

    def draw(self) -> None:
        self.screen.fill(game_config.BACKGROUND_COLOR)
        self.menu_box.draw(self.screen)
