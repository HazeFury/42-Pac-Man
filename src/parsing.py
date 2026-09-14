from pathlib import Path
from pydantic import BaseModel, ValidationError, Field
import json
import sys


class Setup(BaseModel):
    highscore_filename: str = Field(gt=0, default="highscore.json")
    level: int = 10
    width: int = 30
    height: int = 30
    lives: int = 3
    pacgum: int = 42
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    seed: int = 42
    level_max_time: int = 90


class JsonCleaning:
    def __init__(self, filename: str) -> None:
        self.path = Path(filename)

    def open_file(self) -> Setup:
        forbiden_char = ("#", "//")

        clean_json = []
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                lines = f.read()
                for line in lines:
                    if line.strip().startswith(forbiden_char):
                        continue
                    else:
                        clean_json.append(line)
            conf = "".join(clean_json)
            final_json = eval(conf)

            config = json.load(final_json)
            data = Setup(**config)
            return data
        except FileNotFoundError as e:
            print(f"File {self.path} not found {e}")
            sys.exit(1)
