"""
Game configuration constants.
"""

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60
LEVEL_TIME_LIMIT = 10  # Time limit in seconds

# RGB Colors
BACKGROUND_COLOR = (10, 10, 10)
BUTTON_HOVER_COLOR = (100, 100, 255)

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
VIOLET = (238, 130, 238)

# Dictionary to easily fetch colors by string name
COLORS: dict[str, tuple[int, int, int]] = {
    "BLUE": BLUE,
    "WHITE": WHITE,
    "BLACK": BLACK,
    "RED": RED,
    "GREEN": GREEN,
    "YELLOW": YELLOW,
    "ORANGE": ORANGE,
    "VIOLET": VIOLET,
}

# Dictionary to define sizes (width, height)
BUTTON_SIZES: dict[str, tuple[int, int]] = {
    "small": (100, 40),
    "medium": (200, 60),
    "large": (300, 80),
}
