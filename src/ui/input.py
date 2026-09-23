import pygame

from utils import game_config


class TextInput:
    """
    A text input component allowing the user to type alphanumeric characters.
    Complies with the UIElement protocol to be used inside a Box layout.
    """

    def __init__(
        self,
        pos_y: str,
        pos_x: str,
        width: int = 250,
        height: int = 50,
        max_length: int = 10,
    ) -> None:
        self.text: str = ""
        self.max_length: int = max_length
        self.active: bool = True

        self.width: int = width
        self.height: int = height

        self._pos_x_keyword: str = pos_x
        self._pos_y_keyword: str = pos_y

        self.x: int = self._resolve_x()
        self.y: int = self._resolve_y()

        # Pygame font setup
        self.font = pygame.font.SysFont(None, 36)
        self.text_surface: pygame.Surface = self.font.render(
            self.text, True, game_config.WHITE
        )

        # Colors for focus states
        self.color_active = game_config.BLUE
        self.color_passive = game_config.WHITE
        self.color_error = game_config.RED
        self.current_color = self.color_passive

    def _resolve_x(self) -> int:
        """Calculate the absolute X coordinate."""
        if self._pos_x_keyword == "left":
            return 50
        elif self._pos_x_keyword == "right":
            return game_config.WINDOW_WIDTH - self.width - 50
        return (game_config.WINDOW_WIDTH - self.width) // 2

    def _resolve_y(self) -> int:
        """Calculate the absolute Y coordinate."""
        if self._pos_y_keyword == "top":
            return 50
        elif self._pos_y_keyword == "bottom":
            return game_config.WINDOW_HEIGHT - self.height - 50
        return (game_config.WINDOW_HEIGHT - self.height) // 2

    def get_value(self) -> str:
        """
        Returns the current string typed in the input.
        Useful to pass the player's name to the highscore system.
        """
        return self.text

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handles mouse clicks to focus/unfocus the input,
        and captures keyboard typing.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if mouse clicked inside the input box bounding area
            if (
                self.x <= event.pos[0] <= self.x + self.width
                and self.y <= event.pos[1] <= self.y + self.height
            ):
                self.active = True
            else:
                self.active = False

            # Update border color based on focus state
            self.current_color = (
                self.color_active if self.active else self.color_passive
            )

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                # Remove the last character
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                # Pressing Enter unfocuses the input
                self.active = False
                self.current_color = self.color_passive
            else:
                # Subject rule: Max 10 characters
                if len(self.text) < self.max_length:
                    # Subject rule: Alphanumeric and spaces only
                    if event.unicode.isalnum() or event.unicode == " ":
                        self.text += event.unicode

            # Re-render the text surface immediately after any modification
            self.text_surface = self.font.render(
                self.text, True, game_config.WHITE
            )

    def change_color(self, is_error: bool) -> None:
        """Update border color based on error state."""
        if is_error is True:
            self.current_color = self.color_error
        else:
            self.current_color = self.color_passive

    def draw(self, screen: pygame.Surface) -> None:
        """
        Renders the input box border and the typed text.
        """
        # Draw the outline rectangle (thickness = 2)
        pygame.draw.rect(
            screen,
            self.current_color,
            (self.x, self.y, self.width, self.height),
            2,
        )

        # Draw the text inside, vertically centered with a left padding of 10px
        text_y = self.y + (self.height - self.text_surface.get_height()) // 2
        screen.blit(self.text_surface, (self.x + 10, text_y))
