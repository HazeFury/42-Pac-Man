import pygame


class InputManager:
    """
    Acts as the Controller in the MVC architecture.
    Translates hardware inputs (keyboard/gamepads) into abstract game commands.
    """

    def __init__(self) -> None:
        # We could initialize gamepad support here in the future
        pass

    def get_movement_intention(self) -> str:
        """
        Reads the current keyboard state and returns a unified direction
        string. Supports both Arrow keys and WASD/ZQSD configurations.
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_z]:
            return "UP"
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            return "DOWN"
        if keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_q]:
            return "LEFT"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            return "RIGHT"

        return "NONE"

    def is_pause_pressed(self, events: list[pygame.event.Event]) -> bool:
        """
        Checks if the ESCAPE key was pressed in the given frame events.
        """
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True
        return False

    def get_cheat_actions(self, events: list[pygame.event.Event]) -> list[str]:
        """
        Detects cheat key presses (F1 to F5) from the event loop.
        Returns a list of triggered cheat action names.
        """
        actions: list[str] = []
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    actions.append("INVINCIBILITY")
                elif event.key == pygame.K_F2:
                    actions.append("FREEZE_GHOSTS")
                elif event.key == pygame.K_F3:
                    actions.append("SPEED_BOOST")
                elif event.key == pygame.K_F4:
                    actions.append("EXTRA_LIFE")
                elif event.key == pygame.K_F5:
                    actions.append("SKIP_LEVEL")
        return actions
