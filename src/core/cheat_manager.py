from core.game_engine import GameEngine


class CheatManager:
    """
    Manages cheat states and operations for peer-review / debugging.
    Applies effects directly to GameEngine and its entities.
    """

    def __init__(self, game_engine: GameEngine) -> None:
        self.game_engine = game_engine

        # Cheat states (toggles)
        self.is_invincible: bool = False
        self.is_ghost_frozen: bool = False
        self.is_speed_boosted: bool = False

        # Memorize normal player move delay to toggle speed back
        self.normal_move_delay: float = self.game_engine.player.move_delay
        self.boosted_move_delay: float = 0.04  # Faster speed (normal is 0.1)

    def handle_actions(self, actions: list[str]) -> None:
        """Dispatches cheat actions received from InputManager."""
        for action in actions:
            if action == "INVINCIBILITY":
                self.toggle_invincibility()
            elif action == "FREEZE_GHOSTS":
                self.toggle_freeze_ghosts()
            elif action == "SKIP_LEVEL":
                self.skip_level()
            elif action == "EXTRA_LIFE":
                self.add_extra_life()
            elif action == "SPEED_BOOST":
                self.toggle_speed_boost()

    def toggle_invincibility(self) -> None:
        self.is_invincible = not self.is_invincible

    def toggle_freeze_ghosts(self) -> None:
        self.is_ghost_frozen = not self.is_ghost_frozen

    def toggle_speed_boost(self) -> None:
        self.is_speed_boosted = not self.is_speed_boosted
        if self.is_speed_boosted:
            self.game_engine.player.move_delay = self.boosted_move_delay
        else:
            self.game_engine.player.move_delay = self.normal_move_delay

    def add_extra_life(self) -> None:
        self.game_engine.player.lives += 1

    def skip_level(self) -> None:
        for row in self.game_engine.maze.grid:
            for cell in row:
                cell.pacgum = False
                cell.super_pacgum = False
