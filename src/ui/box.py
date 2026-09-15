from typing import Protocol

import pygame

from utils import game_config


class UIElement(Protocol):
    """
    Protocol defining the mandatory interface for any component
    that wants to be placed inside a Box.
    """

    x: int
    y: int
    width: int
    height: int

    def draw(self, screen: pygame.Surface) -> None: ...

    def handle_event(self, event: pygame.event.Event) -> None: ...


class Box:
    """
    A flexbox-like container to align UI components vertically or horizontally.
    """

    def __init__(
        self,
        pos_y: str,
        pos_x: str,
        layout: str = "vertical",
        spacing: int = 20,
    ) -> None:
        self._pos_x_keyword = pos_x
        self._pos_y_keyword = pos_y
        self.layout = layout
        self.spacing = spacing
        self.children: list[UIElement] = []

        # Bounding box of the container (calculated automatically)
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

    def add_child(self, child: UIElement) -> None:
        """Add a UI component to the box and recalculate the layout."""
        self.children.append(child)
        self.update_layout()

    def update_layout(self) -> None:
        """
        Calculate the total bounding box size and position all children.
        This overrides the individual x/y coordinates of the children.
        """
        if not self.children:
            return

        # 1. Calculate the total width and height of the Box
        if self.layout == "vertical":
            self.width = max(child.width for child in self.children)
            self.height = sum(
                child.height for child in self.children
            ) + self.spacing * (len(self.children) - 1)
        else:  # horizontal
            self.width = sum(
                child.width for child in self.children
            ) + self.spacing * (len(self.children) - 1)
            self.height = max(child.height for child in self.children)

        # 2. Position the Box itself on the screen
        self.x = self._resolve_x()
        self.y = self._resolve_y()

        # 3. Assign absolute positions to each child
        current_x = self.x
        current_y = self.y

        for child in self.children:
            if self.layout == "vertical":
                # Center child horizontally within the box
                child.x = self.x + (self.width - child.width) // 2
                child.y = current_y
                current_y += child.height + self.spacing
            else:
                # Center child vertically within the box
                child.x = current_x
                child.y = self.y + (self.height - child.height) // 2
                current_x += child.width + self.spacing

    def _resolve_x(self) -> int:
        """Calculate the absolute X coordinate for the Box."""
        if self._pos_x_keyword == "left":
            return 50
        elif self._pos_x_keyword == "right":
            return game_config.WINDOW_WIDTH - self.width - 50
        else:  # default to "center"
            return (game_config.WINDOW_WIDTH - self.width) // 2

    def _resolve_y(self) -> int:
        """Calculate the absolute Y coordinate for the Box."""
        if self._pos_y_keyword == "top":
            return 50
        elif self._pos_y_keyword == "bottom":
            return game_config.WINDOW_HEIGHT - self.height - 50
        else:  # default to "center"
            return (game_config.WINDOW_HEIGHT - self.height) // 2

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Propagate events to all children (useful for buttons inside the box).
        """
        for child in self.children:
            child.handle_event(event)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw all children."""
        # Note: We don't draw the Box itself (it's invisible), just its
        # children. But you could add a pygame.draw.rect here if you wanted a
        # background behind the group!
        for child in self.children:
            child.draw(screen)
