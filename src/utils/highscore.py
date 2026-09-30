import sys
from pathlib import Path

from pydantic import ValidationError

from src.utils.parsing import Highscore, PlayerScore, config


class HighScoreManager:
    """Manages loading and saving highscores from and to JSON."""

    def __init__(self) -> None:
        """Initialize the highscore file path."""
        filename = config.highscore_filename
        if getattr(sys, "frozen", False):
            self.score_path = Path(sys.executable).parent / filename
        else:
            self.score_path = Path(filename)

    def read_highscore(self) -> Highscore:
        """Read and return highscores from disk as a Highscore instance."""
        if not self.score_path.exists():
            return Highscore()
        try:
            content = self.score_path.read_text(encoding="utf-8")
            return Highscore.model_validate_json(content)
        except (ValidationError, ValueError):
            return Highscore()

    def write_highscore(self, name: str, score: int) -> None:
        """Append a new score record and write updated highscores to disk."""
        highscore = self.read_highscore()
        new_score = PlayerScore(name=name, score=score)
        highscore.scores.append(new_score)
        json_data = highscore.model_dump_json(indent=2)
        self.score_path.write_text(json_data, encoding="utf-8")
