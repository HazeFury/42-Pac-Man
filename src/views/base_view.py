from abc import ABC, abstractmethod

import pygame


class BaseView(ABC):
    """
    Abstract base class enforcing a standard interface for all game views.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        # Variable to tell the main loop if we need to switch view
        self.next_view: str | None = None

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """Process all Pygame events (keyboard, mouse)."""

    @abstractmethod
    def update(self) -> None:
        """Update the logic and state of the view."""

    @abstractmethod
    def draw(self) -> None:
        """Render all graphical elements of the view to the screen."""
