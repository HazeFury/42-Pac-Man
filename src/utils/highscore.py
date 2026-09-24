import sys
from pathlib import Path

from pydantic import ValidationError

from utils.parsing import Highscore, Player_score, config


class HighScoreManager:
    def __init__(self) -> None:
        filename = config.highscore_filename
        if getattr(sys, "frozen", False):
            self.score_path = Path(sys.executable).parent / filename
        else:
            self.score_path = Path(filename)

    def read_highscore(self) -> Highscore:
        if not self.score_path.exists():
            return Highscore()
        try:
            content = self.score_path.read_text(encoding="utf-8")
            return Highscore.model_validate_json(content)
        except (ValidationError, ValueError):
            return Highscore()

    def write_highscore(self, name: str, score: int) -> None:
        highscore = self.read_highscore()
        new_score = Player_score(name=name, score=score)
        highscore.scores.append(new_score)
        json_data = highscore.model_dump_json(indent=2)
        self.score_path.write_text(json_data, encoding="utf-8")
