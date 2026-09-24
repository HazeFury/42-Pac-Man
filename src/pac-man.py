import sys

import pygame

from core.cheat_manager import CheatManager
from core.game_engine import GameEngine
from utils import game_config
from views.end_game_view import EndGameView
from views.game_view import GameView
from views.highscore_view import HighScoreView
from views.menu_view import MenuView


def main() -> None:
    """
    Main entry point of the application.
    Initializes the Pygame window and manages the view state machine.
    """
    try:
        # 1. Initialize the Pygame engine
        pygame.init()

        # 2. Create the unique Window (The Canvas)
        screen = pygame.display.set_mode(
            (game_config.WINDOW_WIDTH, game_config.WINDOW_HEIGHT)
        )
        pygame.display.set_caption("Pac-Man 42")
        clock = pygame.time.Clock()

        # 3. Instantiate all our views (The Painters)
        # We pass the shared 'screen' to all of them.
        game_engine = GameEngine()
        cheat_manager = CheatManager(game_engine)
        game_engine.cheat_manager = cheat_manager

        views = {
            "MENU": MenuView(screen, game_engine),
            "GAME": GameView(screen, game_engine),
            "WIN": EndGameView(screen, game_engine, is_victory=True),
            "GAMEOVER": EndGameView(screen, game_engine, is_victory=False),
            "SCORE": HighScoreView(screen),
        }

        # Set the initial state
        current_state = "MENU"
        active_view = views[current_state]

        # 4. Main Loop
        running = True
        while running:
            # --- A. Retrieve all events once ---
            # We fetch events here and pass the list to the view.
            # This prevents bugs where multiple views consume events
            # concurrently.
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            # --- B. Delegate work to the active view ---
            # --- B. Handle Cheats in Game ---
            if current_state == "GAME":
                actions = game_engine.input_manager.get_cheat_actions(events)
                cheat_manager.handle_actions(actions)

            # --- C. Delegate work to the active view ---
            active_view.handle_events(events)
            active_view.update()
            active_view.draw()

            # --- C. Check if the view requested a state change ---
            if active_view.next_view is not None:
                # Change the state
                current_state = active_view.next_view
                active_view = views[current_state]

                # Reset the next_view property of the OLD view so it doesn't
                # instantly trigger a change next time we come back to it.
                for view in views.values():
                    view.next_view = None

            # --- D. Render to screen & Tick ---
            pygame.display.flip()
            clock.tick(game_config.FPS)

        # Clean exit
        pygame.quit()
        sys.exit()
    except KeyboardInterrupt:
        print(
            "\n\033[93m[INFO] User interrupt "
            "(Ctrl+C). Program closing...\033[0m",
            file=sys.stderr,
        )
        pygame.quit()
        sys.exit(0)

    except Exception as e:
        print(f"\033[91m[FATAL ERROR]\033[0m {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
