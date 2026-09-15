from collections.abc import Callable

import pygame

from utils import game_config


class Button:
    """
    Button component of different size, positions and color.
    It triggers a callback function when clicked.
    """

    def __init__(
        self,
        pos_y: str,
        pos_x: str,
        text: str,
        func: Callable[[], None],
        color: str,
        size: str = "medium",
    ) -> None:
        self.text = text
        self.func = func

        # Fetch actual data from config dictionaries
        self.color = game_config.COLORS.get(color.upper(), game_config.WHITE)
        self.width, self.height = game_config.BUTTON_SIZES.get(
            size, game_config.BUTTON_SIZES["medium"]
        )

        # Calculate dynamic positions
        self.x = self._resolve_x(pos_x)
        self.y = self._resolve_y(pos_y)

        # Pygame font setup (MLX equivalent: default system font)
        self.font = pygame.font.SysFont(None, 36)

    def _resolve_x(self, pos_x: str) -> int:
        """Calculate the absolute X coordinate based on the keyword."""
        if pos_x == "left":
            return 20
        elif pos_x == "right":
            return game_config.WINDOW_WIDTH - self.width - 20
        else:  # default to "center"
            return (game_config.WINDOW_WIDTH - self.width) // 2

    def _resolve_y(self, pos_y: str) -> int:
        """Calculate the absolute Y coordinate based on the keyword."""
        if pos_y == "top":
            return 20
        elif pos_y == "bottom":
            return game_config.WINDOW_HEIGHT - self.height - 20
        else:  # default to "center"
            return (game_config.WINDOW_HEIGHT - self.height) // 2

    def is_hovering(self, mouse_pos: tuple[int, int]) -> bool:
        """
        Return True if the cursor hovers this button.
        """
        mouse_x, mouse_y = mouse_pos
        return (
            self.x <= mouse_x <= self.x + self.width
            and self.y <= mouse_y <= self.y + self.height
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Trigger the callback function if the button is clicked.
        Should be called inside the main event loop.
        """
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.is_hovering(event.pos)
        ):
            self.func()

    def draw(self, screen: pygame.Surface) -> None:
        """
        Render the button and its text on the provided screen.
        """
        mouse_pos = pygame.mouse.get_pos()

        # Swap color if mouse is hovering
        current_color = (
            game_config.BUTTON_HOVER_COLOR
            if self.is_hovering(mouse_pos)
            else self.color
        )

        # Draw background rectangle
        pygame.draw.rect(
            screen, current_color, (self.x, self.y, self.width, self.height)
        )

        # Draw centered text
        text_surf = self.font.render(self.text, True, game_config.BLACK)
        text_rect = text_surf.get_rect(
            center=(self.x + self.width // 2, self.y + self.height // 2)
        )
        screen.blit(text_surf, text_rect)
