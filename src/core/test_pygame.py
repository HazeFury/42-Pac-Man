import sys

import pygame

# Constants configuration
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
LEVEL_TIME_LIMIT = 10  # Time limit in seconds

# RGB Colors
BACKGROUND_COLOR = (10, 10, 10)
PLAYER_COLOR = (255, 255, 0)
BUTTON_COLOR = (50, 50, 150)
BUTTON_HOVER_COLOR = (100, 100, 255)
TEXT_COLOR = (255, 255, 255)
TITLE_COLOR = (255, 255, 0)


def main() -> None:
    """
    Main function containing the state machine, text rendering,
    and a countdown timer for the game loop.
    """
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pygame Sandbox - Menu & Game")
    clock = pygame.time.Clock()

    # 1. Font initialization
    # We create two different font sizes for the title and the UI elements
    title_font = pygame.font.SysFont(None, 100)
    ui_font = pygame.font.SysFont(None, 48)

    current_state = "MENU"

    player_x = 400
    player_y = 300
    player_size = 30
    player_speed = 15

    button_width = 200
    button_height = 60
    button_x = (WINDOW_WIDTH - button_width) // 2
    button_y = (WINDOW_HEIGHT - button_height) // 2

    # Variable to store the exact timestamp when the game starts
    game_start_time = 0

    running = True
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if current_state == "MENU":
                    if (
                        button_x <= mouse_x <= button_x + button_width
                        and button_y <= mouse_y <= button_y + button_height
                    ):
                        # Switch state to GAME
                        current_state = "GAME"
                        pygame.display.set_mode((1200, 1600))
                        # Record the system time (in milliseconds) at the exact moment we click PLAY
                        game_start_time = pygame.time.get_ticks()

        screen.fill(BACKGROUND_COLOR)

        if current_state == "MENU":
            # --- Rendering the Title ---
            # Create an image (Surface) containing the text
            title_surface = title_font.render("Pac Man", True, TITLE_COLOR)
            # Center the text horizontally, near the top
            title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 150))
            # Blit (draw) the text surface onto the main screen
            screen.blit(title_surface, title_rect)

            # Button logic
            is_hovering = (
                button_x <= mouse_x <= button_x + button_width
                and button_y <= mouse_y <= button_y + button_height
            )
            current_btn_color = BUTTON_HOVER_COLOR if is_hovering else BUTTON_COLOR
            pygame.draw.rect(
                screen,
                current_btn_color,
                (button_x, button_y, button_width, button_height),
            )

            text_surface = ui_font.render("PLAY", True, TEXT_COLOR)
            text_rect = text_surface.get_rect(
                center=(button_x + button_width // 2, button_y + button_height // 2)
            )
            screen.blit(text_surface, text_rect)

        elif current_state == "GAME":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player_y -= player_speed
            if keys[pygame.K_DOWN]:
                player_y += player_speed
            if keys[pygame.K_LEFT]:
                player_x -= player_speed
            if keys[pygame.K_RIGHT]:
                player_x += player_speed

            pygame.draw.rect(
                screen, PLAYER_COLOR, (player_x, player_y, player_size, player_size)
            )

            # --- Timer Logic ---
            # Get the current system time in milliseconds
            current_time = pygame.time.get_ticks()

            # Calculate how many seconds have passed since we entered the GAME state
            elapsed_seconds = (current_time - game_start_time) // 1000

            # Calculate remaining time (max(0, ...) ensures it doesn't go below 0)
            remaining_time = max(0, LEVEL_TIME_LIMIT - elapsed_seconds)

            # Render the timer string
            timer_text = f"Time: {remaining_time}"
            timer_surface = ui_font.render(timer_text, True, TEXT_COLOR)
            screen.blit(timer_surface, (10, 10))

            # Bonus feature: if the timer hits 0, return to menu and reset position
            if remaining_time == 0:
                current_state = "MENU"
                player_x = 400
                player_y = 300

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
