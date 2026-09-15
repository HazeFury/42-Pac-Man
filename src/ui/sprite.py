from typing import List, Union

import pygame

from utils import game_config


class Sprite:
    """
    A component to render static or animated images.
    It can be placed in a UI Box (using string positions)
    or freely in the game world (using int coordinates).
    """

    def __init__(
        self,
        pos_y: Union[str, int],
        pos_x: Union[str, int],
        image_paths: List[str],
        animation_speed: float = 0.1,  # Time in seconds between each frame
    ) -> None:

        # 1. Load all images from the provided paths
        self.frames: List[pygame.Surface] = []
        for path in image_paths:
            # convert_alpha() is crucial for performance and handling
            #  transparency (PNGs)
            try:
                img = pygame.image.load(path).convert_alpha()
                self.frames.append(img)
            except FileNotFoundError:
                print(f"Error: Could not load image at {path}")
                # Create a fallback pink square to avoid crashes
                fallback = pygame.Surface((30, 30))
                fallback.fill((255, 0, 255))
                self.frames.append(fallback)

        # Animation state variables
        self.current_frame_index = 0
        self.animation_speed = animation_speed
        self.time_since_last_frame = 0.0

        # Set the active image and get its dimensions
        self.image = self.frames[self.current_frame_index]
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # 2. Position handling (UI keywords or absolute coordinates)
        self._pos_x_raw = pos_x
        self._pos_y_raw = pos_y
        self.x = self._resolve_x(pos_x)
        self.y = self._resolve_y(pos_y)

    def _resolve_x(self, pos_x: Union[str, int]) -> int:
        """
        Resolve X position. Returns the integer if provided, else computes UI
        layout.
        """
        if isinstance(pos_x, int):
            return pos_x
        if pos_x == "left":
            return 50
        if pos_x == "right":
            return game_config.WINDOW_WIDTH - self.width - 50
        return (game_config.WINDOW_WIDTH - self.width) // 2

    def _resolve_y(self, pos_y: Union[str, int]) -> int:
        """
        Resolve Y position. Returns the integer if provided, else computes UI
        layout.
        """
        if isinstance(pos_y, int):
            return pos_y
        if pos_y == "top":
            return 50
        if pos_y == "bottom":
            return game_config.WINDOW_HEIGHT - self.height - 50
        return (game_config.WINDOW_HEIGHT - self.height) // 2

    def update_animation(self, delta_time: float) -> None:
        """
        Update the current frame based on elapsed time.
        Needs to be called in the main update loop with the time passed
        since last frame.
        """
        # If there's only one frame, it's a static image, no need to animate
        if len(self.frames) <= 1:
            return

        self.time_since_last_frame += delta_time

        # When enough time has passed, switch to the next frame
        if self.time_since_last_frame >= self.animation_speed:
            self.time_since_last_frame = 0.0

            # Loop back to 0 when reaching the end of the list
            self.current_frame_index = (self.current_frame_index + 1) % len(
                self.frames
            )
            self.image = self.frames[self.current_frame_index]

    def update_position(self, new_x: int, new_y: int) -> None:
        """Allows game entities (like Pac-Man) to move this sprite."""
        self.x = new_x
        self.y = new_y

    def handle_event(self, event: pygame.event.Event) -> None:
        """Required to comply with the UIElement protocol."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the current active frame on the screen."""
        screen.blit(self.image, (self.x, self.y))
