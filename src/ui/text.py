import pygame

from utils import game_config


class Text:
    """
    Text component to display strings on the screen with dynamic positioning.
    It supports color fetching from the configuration and dynamic text updates.
    """

    def __init__(
        self,
        pos_y: str,
        pos_x: str,
        text: str,
        color: str,
        font_size: int = 36,
    ) -> None:
        self._pos_x_keyword = pos_x
        self._pos_y_keyword = pos_y
        self.color = game_config.COLORS.get(color.upper(), game_config.WHITE)

        # Pygame font setup (MLX equivalent: default system font)
        self.font = pygame.font.SysFont(None, font_size)

        # Initial rendering and positioning
        self.surface: pygame.Surface
        self.width: int
        self.height: int
        self.x: int
        self.y: int

        self.update_text(text)

    def _resolve_x(self) -> int:
        """Calculate the absolute X coordinate based on the current surface width."""
        if self._pos_x_keyword == "left":
            return 50
        elif self._pos_x_keyword == "right":
            return game_config.WINDOW_WIDTH - self.width - 50
        else:  # default to "center"
            return (game_config.WINDOW_WIDTH - self.width) // 2

    def _resolve_y(self) -> int:
        """Calculate the absolute Y coordinate based on the current surface height."""
        if self._pos_y_keyword == "top":
            return 50
        elif self._pos_y_keyword == "bottom":
            return game_config.WINDOW_HEIGHT - self.height - 50
        else:  # default to "center"
            return (game_config.WINDOW_HEIGHT - self.height) // 2

    def update_text(self, new_text: str) -> None:
        """
        Update the text surface and recalculate positions.
        Crucial for dynamic elements like score or timers.
        """
        # 1. Render the new text into an image (Surface)
        self.surface = self.font.render(new_text, True, self.color)

        # 2. Get the new physical dimensions
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()

        # 3. Recalculate X and Y so it remains properly aligned/centered
        self.x = self._resolve_x()
        self.y = self._resolve_y()

    def draw(self, screen: pygame.Surface) -> None:
        """
        Render the text surface on the provided screen.
        """
        screen.blit(self.surface, (self.x, self.y))
